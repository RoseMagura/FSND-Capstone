import os
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
import json

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/casting'
migrate = Migrate(app, db)


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
# def setup_db(app, database_path=database_path):
    
    
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)
#     db.create_all()

cast = db.Table('cast',
    db.Column('actor_id', db.Integer, db.ForeignKey('Actors.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movies.id'), primary_key=True))
# class Cast(db.Model):
#     __tablename__ = 'cast'

#     actor_id = db.Column(db.Integer, db.ForeignKey('Actors.id'))
#     movie_id = db.Column(db.Integer, db.ForeignKey('Movies.id')) 
#     actor = db.relationship('Actor', back_populates=)

#     def __init__(self, actor_id, movie_id):
#         self.actor_id = actor_id
#         self.movie_id = movie_id

#     def format(self):
#         return{
#             'id': self.id,
#             'actor_id': self.actor_id,
#             'movie_id': self.movie_id
#         } 
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

    def format(self):
        return{
            'id': self.id,
            'name': self.name, 
            'age': self.age,
            'gender': self.gender, 
            'movies': [m.name for m in self.movies]
        } 


   
   