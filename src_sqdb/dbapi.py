# %%
import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql.sqltypes import JSON

from .enums import ResourceType, SeqType, SequencerOutFormat


Base = declarative_base()


def get(session, model, **kwargs):
    '''
    gets first object of <model> with paramaters from DB
    '''
    return session.query(model).filter_by(**kwargs).first()


def get_or_create(session, model, **kwargs):
    '''
    gets first object of <model> with paramaters from DB or creates new
    should be commited later
    '''
    instance = session.query(model).filter_by(**kwargs).first()

    if instance is not None:
        return instance
    else:
        return model(**kwargs)


class Project(Base):
    '''
    table of projects information
    '''
    __tablename__ = "project"

    id = sa.Column(sa.String(100), primary_key=True)
    launches = relationship("Launch", back_populates="project")

    def __repr__(self) -> str:
        return f"<Project {self.id}>"

    def get_biosamples(self, session):
        res = []
        sample_prj = session\
            .query(Launch)\
            .filter(Launch.project_id == self.id)\
            .all()

        for sp in sample_prj:
            res.append(sp.biosample)
        return res


class BioSample(Base):
    '''
    biological sample
    '''
    __tablename__ = "biosample"
    id = sa.Column(sa.String, primary_key=True)
    type = sa.Column(sa.String)

    def __repr__(self) -> str:
        return f"<BioSample {self.id}>"

    def append_to_project(self, session, project):
        project.add_sample(session, [self])

    def append_to_flowcell(self, session, flowcell):
        return flowcell.create_binding(session, self)


class Sequencer(Base):
    __tablename__ = "sequencer"

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    company = sa.Column(sa.String)
    name = sa.Column(sa.String)
    output_type = sa.Column(ENUM(SequencerOutFormat))


class Flowcell(Base):
    '''
    unique flowcell
    '''
    __tablename__ = "flowcell"
    id = sa.Column(sa.String, primary_key=True)

    sequencing_type = sa.Column(sa.String)
    sequencing_subtype = sa.Column(sa.String)

    sequencing_data_path = sa.Column(sa.String)

    sequencer_id = sa.Column(sa.Integer, sa.ForeignKey("sequencer.id"))

    sample_sheet = sa.Column(sa.String)
    sample_sheet_hash = sa.Column(sa.String)

    sequencer = relationship("Sequencer")

    launches = relationship("Launch")

    def add_biosaple(self, session, biosample, replica):
        lnch = get_or_create(
            session,
            Launch,
            flowcell=self,
            biosample=biosample,
            replica=replica
        )
        self.launches.append(lnch)

        return lnch

    def get_biosamples(self, session):
        res = []
        launches = session.query(Launch).filter(
            Launch.flowcell_id == self.id).all()
        for launch in launches:
            res.append(launch.biosample)
        return res

    def get_launches(self, session):
        launches = session.query(Launch).filter(
            Launch.flowcell_id == self.id).all()
        return launches


class Resource(Base):
    '''
    table of all data files from launch

    as example fastq and bam files from biosample X sequenced in flowcell Y
    '''
    __tablename__ = "resource"
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    path = sa.Column(sa.String)
    data_type = sa.Column(ENUM(ResourceType))
    launch_id = sa.Column(sa.Integer, sa.ForeignKey("launch.id"))
    launch = relationship("Launch")
    metrics = sa.Column(JSON)

    def to_dict(self):
        return {
            "path": self.path,
            "data_type": self.data_type.value,
            "metrics": self.metrics
        }

    def get_metrics(self):
        self.metrics = None


class Launch(Base):
    '''
    table of launches(biosample that was in sequencer launch)
    '''
    __tablename__ = "launch"
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    flowcell_id = sa.Column(sa.String, sa.ForeignKey("flowcell.id"))
    flowcell = relationship("Flowcell")

    biosample_id = sa.Column(sa.String, sa.ForeignKey("biosample.id"))
    biosample = relationship("BioSample")

    replica = sa.Column(sa.String)

    project_id = sa.Column(sa.String, sa.ForeignKey("project.id"))
    project = relationship("Project")

    def add_project(self, session, project_name):
        prj = get_or_create(
            session,
            Project,
            id=project_name
        )
        self.project = prj

        session.merge(prj)

    def get_resources(self, session):
        return session\
            .query(Resource)\
            .filter(Resource.launch_id == self.id)\
            .all()
