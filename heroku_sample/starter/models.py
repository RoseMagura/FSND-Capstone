import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json

# os.environ['DATABASE_URL'] = 'postgres://postgres:1@localhost:5432/herokutest'
# database_path = os.environ['DATABASE_URL']
database_path = 'postgres://rbzkztrfwjyghb:96e6932b69f21b236db0420120ac32818cd3d99d9b00f8d1fc6e4a20d8c7bb71@ec2-52-22-216-69.compute-1.amazonaws.com:5432/d75ujhmqfldjfu'
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
Person
Have title and release year
'''
class Person(db.Model):  
  __tablename__ = 'People'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'catchphrase': self.catchphrase}