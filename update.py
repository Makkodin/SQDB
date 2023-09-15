import sqlalchemy as sa
from tqdm import tqdm
import os
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database

from sqdb.resources import get_samplesheet_info, get_pattern_resources, \
                        FastqResource, RnaBamResource, TenXResource
from sqdb.added_params import get_replics
from sqdb.enums import ResourceType
from sqdb.sample_sheet import SampleSheet
from sqdb.dbapi import get_or_create, Flowcell, BioSample,\
    Launch, SeqType, Base, Project

load_dotenv()

DATABASE = os.getenv('DATABASE')
USERNAME = os.getenv('DATABASE_USERNAME')
PASSWORD = os.getenv('DATABASE_PASSWORD')
PORT = os.getenv('DATABASE_PORT')
HOST = os.getenv('DATABASE_HOST')

engine = sa.create_engine(
    f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}',
    echo=False
)
if not database_exists(engine.url):
    create_database(engine.url)

#engine.execute('CREATE EXTENSION IF NOT EXISTS "fuzzystrmatch";')    

s = sa.orm.sessionmaker()
s.configure(bind=engine)
session = s()
session.no_autoflush
Base.metadata.create_all(engine)

def update_database():

    pattern_list = ['10X_G'] # 'TSO500', '10X_G', '10X_SC_RNA', '10X_SC_ATAC', 'RNASeq'

    sample_sheets = []

    for pattern_name in pattern_list: 
        sample_sheets = sample_sheets + get_samplesheet_info(pattern_name)

    for ss_info in tqdm(sample_sheets):

        ss_path             = ss_info['SampleSheet']
        ss_name             = ss_info['SampleSheet_name']
        flowcell_name       = ss_info['Flowcell']
        pool                = ss_info['Pool']
        type_seq            = ss_info['Type']
        subtype_seq         = ss_info['Subtype'] 

        sample_sheet = SampleSheet(ss_path)

        flowcell = get_or_create(session, 
                                 Flowcell, 
                                 id=flowcell_name)
        session.add(flowcell)

        flowcell.sample_sheet = ss_name
        flowcell.sequencing_data_path = ss_path

        flowcell.sequencing_type = type_seq
        flowcell.sequencing_subtype = subtype_seq

        resources = get_pattern_resources(ss_path,
                                flowcell_name,
                                sample_sheet,
                                pool)

        
        for sample_content in sample_sheet.biosamples:
            
            biosample_name, replica = get_replics(sample_content)
            biosample = get_or_create(session, 
                                      BioSample, 
                                      id=biosample_name)
            session.add(biosample)
            lnch = flowcell.add_biosaple(session, 
                                         biosample=biosample, 
                                         replica=replica)
            session.add(lnch)
            if sample_content[2] is not None:
                lnch.add_project(session, 
                                 project_name=sample_content[2])
            if biosample_name in resources['fastqs']:
                for fastq_file in resources['fastqs'][biosample_name]:

                    fastq_resources = get_or_create(session, 
                                                    FastqResource, 
                                                    data_type=ResourceType.FASTQ, 
                                                    path=fastq_file)
                    fastq_resources.get_metrics()
                    fastq_resources.launch = lnch
                    session.merge(fastq_resources)
            if biosample_name in resources['metrics']:
                if type_seq == '10X': 
                    res = TenXResource
                    data_type = ResourceType.CSV
                elif type_seq == 'RNASeq':
                    res = RnaBamResource
                    data_type = ResourceType.BAM
                for metrics_file in resources['metrics'][biosample_name]:

                    metrics_resources = get_or_create(session, 
                                                      res, 
                                                      data_type=data_type, 
                                                      path=metrics_file)
                    metrics_resources.get_metrics()
                    metrics_resources.launch = lnch
                    session.merge(metrics_resources)
            session.commit()
        session.commit()
    session.commit()

update_database()