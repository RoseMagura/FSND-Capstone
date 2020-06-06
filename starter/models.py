import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
import json

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
# def setup_db(app, database_path=database_path):
    
#     
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)
#     db.create_all()

'''
Movie
Attributes include title and release date
'''
class Movie(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    release_date = db.Column(db.Integer)
    actor = db.relationship('Cast', backref='Movies', lazy=True)
 
    def __init__(self, name, release_date, stars):
        self.name = name
        self.release_date = release_date
        self.stars = stars

    def format(self):
        return{
            'id': self.id,
            'name': self.name, 
            'release_date': self.release_date, 
            'stars': self.stars
        }    

'''
Actor
Attributes include name, age, and gender
'''    
class Actor(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    movies = db.relationship('Cast', backref='Actors', lazy=True)

    def __init__(self, name, age, gender, movies):
        self.name = name
        self.age = age
        self.gender = gender
        self.movies = movies

    # def format(self):
    #     return{
    #         'id': self.id,
    #         'name': self.name, 
    #         'age': self.age,
    #         'gender': self.gender,
    #     } 


class Cast(db.Model):
    __tablename__ = 'Cast'

    id = db.Column(db.Integer, primary_key=True)    
    actor_id = db.Column(db.Integer, db.ForeignKey(Actor.id))
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id)) 

    def format(self):
        return{
            'id': self.id,
            'actor_id': self.actor_id,
            'movie_id': self.movie_id
        }    

# app.config["SQLALCHEMY_DATABASE_URI"] = database_path

db.app = app
# db.init_app(app)
# db.create_all()        