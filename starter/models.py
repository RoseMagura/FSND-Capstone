import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json

#database path

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Movie
Attributes include title and release date
'''
class Movie(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    release_date = Column(Integer)

    def __init__(self, name, release_date):
        self.name = name
        self.release_date = release_date

    def format(self):
        return{
            'id': self.id,
            'name': self.name, 
            'release_date': self.release_date
        }    

'''
Actor
Attributes include name, age, and gender
'''    
class Actor(db.Model):
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender

    def format(self):
        return{
            'id': self.id,
            'name': self.name, 
            'release_date': self.release_date
        } 