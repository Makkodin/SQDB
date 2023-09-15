import sqlalchemy as sa
import itertools

from flask import Flask, jsonify, request

from flask_cors import CORS
from flask.helpers import send_from_directory
from dotenv import load_dotenv

import sqdb.dbapi as dbapi

import psycopg2
import os

load_dotenv()

# PostgreSQL Database учетные данные, загруженные из файла .env
DATABASE = os.getenv('DATABASE')
USERNAME = os.getenv('DATABASE_USERNAME')
PASSWORD = os.getenv('DATABASE_PASSWORD')
PORT = os.getenv('DATABASE_PORT')
HOST = os.getenv('DATABASE_HOST')

app = Flask(__name__, 
            static_url_path='',
            static_folder="front/build")

# CORS реализовано таким образом, чтобы мы не получали ошибок 
# при попытке доступа к серверу с другого расположения сервера
CORS(app, resources={r"/api/*": {"origins": "*"}})

# объект Engine, который объект Session будет использован для
# соединения с ресурсами
engine = sa.create_engine(
    f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}',
    echo=True
)

# создание конфигурации класса Session
s = sa.orm.sessionmaker(bind=engine)
session = s()

dbapi.Base.metadata.create_all(engine)

#----------------------------------------------------------------------------
# Домашняя страница будет содержать в себе контент "index.html" 
# из статичной папки
@app.route("/", defaults={'path': ''})
def index(path):
    return send_from_directory(app.static_folder, "index.html")

# Поведение при ошибке 404 - вызов контента "index.html"
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')
#----------------------------------------------------------------------------
#                                   PROJECTS

# Запрос GET колонку id из таблицы Project 
@app.route("/api/projects", methods=["GET"])
def get_all_projects():

    res = [r[0] for r in session.query(dbapi.Project.id).all()]
    print('-------')
    print('Projects :')
    print(res)
    print('-------')
    return jsonify([res[0] for res in session.query(dbapi.Project.id)])

# Делаем запрос GET в БД для получения всех ячеек по выбранному проекту
@app.route("/api/projects/<string:project_id>", methods=["GET"])
def get_project_info(project_id):

    resp = [(r[0], r[1], r[2]) for r in session.query(  dbapi.Flowcell.id, 
                                                        dbapi.Flowcell.sequencing_type,
                                                        dbapi.Flowcell.sequencing_subtype)
                                                
                                                .filter(dbapi.Launch.flowcell_id == dbapi.Flowcell.id)
                                                .filter(project_id == dbapi.Launch.project_id)
                                                .all()]

    new_resp = []
    for elem in resp:
        if elem not in new_resp:
            new_resp.append(elem)
    resp = new_resp

    return jsonify(resp)

#----------------------------------------------------------------------------
#                                   SEQ TYPE

@app.route("/api/types", methods=["GET"])
def get_all_types(): 
    res = [r[0] for r in session.query(dbapi.Flowcell.sequencing_subtype).all()]
    res = list(set(res))

    return jsonify(res)

@app.route("/api/types/<string:subtype_seq>", methods=["GET", 'POST'])
def get_all_flowcells(subtype_seq):


    resp = [(r[0], r[1], r[2]) for r in session.query(  dbapi.Flowcell.id, 
                                                        dbapi.Flowcell.sequencing_subtype,
                                                        dbapi.Flowcell.sample_sheet)
                                                
                                                .filter(dbapi.Flowcell.sequencing_subtype == subtype_seq)
                                                #.limit(5)
                                                .all()]

    return jsonify(resp)

#----------------------------------------------------------------------------
#                                   FLOWCELLS

@app.route("/api/flowcells", methods=["GET"])
def get_all_flowcell(): 
    res = [r[0] for r in session.query(dbapi.Flowcell.id).all()]

    return jsonify(res)

# Список всех biosample для ячейки
@app.route("/api/flowcells/<string:flowcell_id>", methods=['GET', 'POST'])
def get_flowcell(flowcell_id):

    flowcell = dbapi.get(session, dbapi.Flowcell, id=flowcell_id)

    if flowcell is None:
        return "Not found", 404
    
    launches = flowcell.get_launches(session)

    resp = []
    for launch in launches:
        resources = []
        for res in launch.get_resources(session):
            resources.append(res.to_dict())

        resp.append({"biosample_name": launch.biosample_id, 
                     "replica": launch.replica, 
                     "resources": resources})
        
    return jsonify({
        "name": flowcell.id,
        "seq_subtype":flowcell.sequencing_subtype,
        "sample_sheet": flowcell.sample_sheet,
        "biosamples": resp
    })

# Поисковик по именям ячеек
@app.route("/api/flowcells/search/<string:flowcell_id>", methods=['GET', 'POST'])
def search_flowcell(flowcell_id):
    resp = [(r[0], r[1], r[2]) for r in session.query(  dbapi.Flowcell.id, 
                                                        dbapi.Flowcell.sequencing_type,
                                                        dbapi.Flowcell.sequencing_subtype,
                                                        dbapi.Flowcell.sample_sheet)
                                                        .order_by(
        
                                                sa.func.levenshtein(dbapi.Flowcell.id, 
                                                                    flowcell_id))
                                                                    .limit(5)
                                                                    .all()]
    return jsonify(resp)


# Поисковик по именям образцов
@app.route("/api/flowcells/search/sample_sheet/<string:sample_sheet>", methods=['GET', 'POST'])
def search_flowcell_by_sample_sheet(sample_sheet):
    resp = [(r[0], r[1], r[2]) for r in session.query(  dbapi.Flowcell.id, 
                                                        dbapi.Flowcell.sequencing_type,
                                                        dbapi.Flowcell.sequencing_subtype, 
                                                        dbapi.Flowcell.sample_sheet)
                                                        .order_by(
        
                                                sa.func.levenshtein(dbapi.Flowcell.sample_sheet, 
                                                                    sample_sheet))
                                                                    .limit(5)
                                                                    .all()]
    return jsonify(resp)


#----------------------------------------------------------------------------
#                                   BIOSAMPLES

@app.route("/api/biosamples/search/<string:biosample_id>", methods=['GET', 'POST'])
def search_biosample(biosample_id):
    resp = [r[0] for r in session.query(dbapi.BioSample.id)
                            .order_by(
                    
                    sa.func.levenshtein(dbapi.BioSample.id, 
                                        biosample_id))
                                        .limit(5)
                                        .all()]
    return jsonify(resp)



@app.route("/api/biosamples/<string:biosample_id>")
def get_sample(biosample_id):
    '''
    returns all launches and resources of biosample
    '''
    sample = dbapi.get(session, dbapi.BioSample, id=biosample_id)

    print('---', print(sample), '---', sep='\n')
    if biosample_id is None:
        return "Not found", 404

    flowcells = [
        (cell[0], cell[1], cell[2], cell[3]) for cell in session.query( dbapi.Launch.flowcell_id, 
                                                                        dbapi.Launch.project_id, 
                                                                        dbapi.Flowcell.sequencing_type,
                                                                        dbapi.Flowcell.sequencing_subtype)
                                        
                                                                .filter(dbapi.Flowcell.id == dbapi.Launch.flowcell_id)
                                                                .filter(dbapi.Launch.biosample_id == sample.id)
                                                                .all()]

    return jsonify(
        {   "id": sample.id,
            "type": sample.type,
            "flowcells": flowcells})



#----------------------------------------------------------------------------
#                                   MISC

@app.route("/api/update", methods=["GET", "POST"])
def update():
    print("Processing")
    # process_pattern()
    print("Processed")

    return "ok"

if __name__ == "__main__":
    # process_pattern()
    # pass
    app.run('10.101.12.14', 8087, debug=True)
    pass
