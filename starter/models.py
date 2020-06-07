import os
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
import json

database_name = 'casting'
database_path = 'postgresql://{}:{}@{}/{}'.format(
                            'postgres', 1, 'localhost:5432', database_name)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    
    app = Flask(__name__)
    db = SQLAlchemy(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    migrate = Migrate(app, db)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

cast = db.Table('cast',
    db.Column('actor_id', db.Integer, db.ForeignKey('Actors.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movies.id'), primary_key=True))

'''
Movie
Attributes include title and release date
'''
class Movie(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String())
    release_date = db.Column(db.Integer)
    actors = db.relationship('Actor', secondary=cast, 
        backref=db.backref('Actors', lazy=True))
 
    def __init__(self, name, release_date, actors):
        self.name = name
        self.release_date = release_date
        self.actors = actors

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()        

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'name': self.name, 
            'release_date': self.release_date, 
            'actors': [a.name for a in self.actors]
        }    


'''
Actor
Attributes include name, age, and gender
'''    
class Actor(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    gender = db.Column(db.String())
    movies = db.relationship('Movie', secondary=cast, 
        backref=db.backref('Movies', lazy=True))

    def __init__(self, name, age, gender, movies):
        self.name = name
        self.age = age
        self.gender = gender
        self.movies = movies

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()        

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'name': self.name, 
            'age': self.age,
            'gender': self.gender, 
            'movies': [m.name for m in self.movies]
        } 


   
   