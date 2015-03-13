#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
from app import db

#engine = create_engine('sqlite:///database.db', echo=True)
#db_session = scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=engine))
#db.Model = declarative_base()
#db.Model.query = db_session.query_property()

# Set your classes here.


class Constituency(db.Model):
    __tablename__ = "Constituency"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    boundary = db.Column(db.String(1e5), unique=True)
    children = db.relationship("Results")

    def __init__(self, name):
        self.name = name


class Results(db.Model):
    __tablename__ = "Results"
    id = db.Column(db.Integer, primary_key=True)
    constituency_id = db.Column(db.Integer, db.ForeignKey('Constituency.id'))
    turnout = db.Column(db.Integer)
    numvotes = db.Column(db.Integer)
    year = db.Column(db.Integer)
    children = db.relationship("Candidates")


class Candidates(db.Model):
    __tablename__ = "Candidates"
    id = db.Column(db.Integer, primary_key=True)
    results_id = db.Column(db.Integer, db.ForeignKey('Results.id'))
    turnout = db.Column(db.Integer)
    MPname = db.Column(db.String(120))
    MPparty = db.Column(db.Integer, db.ForeignKey('Party.id'))
    child = db.relationship("Party")
    numvotes = db.Column(db.Integer)
    year = db.Column(db.Integer)


class Party(db.Model):
    __tablename__ = "Party"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))


# Create tables.
# db.Model.metadata.create_all(bind=engine)
