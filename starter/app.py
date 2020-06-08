import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.config.from_object('config.TestConfig')
  setup_db(app)
 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, DELETE')
      response.headers.add('Access-Control-Allow-Credentials', 'true')
      return response

  # @app.route('/')

  @app.route('/movies')
  def get_movies():
    names = []
    for movie in Movie.query.all():
      names.append(movie.name)
    return jsonify({'movies': names})

  @app.route('/movies', methods=['POST'])
  def create_movie():
    body = request.get_json()  
    new_name = body.get('name', None)   
    new_release = body.get('release_date', None) 
    new_actors = body.get('actors', None)
    actor_list = []

    for actor in new_actors:
      new = Actor.query.filter(Actor.name==actor).first()
      # if len(new) = 0:
      #   abort
      actor_list.append(new)
    
    try:
      entry = Movie(name=new_name, release_date=new_release, \
                    actors=actor_list)
      entry.insert()

      return jsonify({
        'success': True, 
        'created': entry.id,
        'total_actors': len(Movie.query.all())
      })

    except Exception as ex:
      print(ex)
      return 'issue'    

  @app.route('/actors')
  def get_actors():
    names = []
    for actor in Actor.query.all():
      names.append(actor.name)
    return jsonify({'actors': names})

  @app.route('/actors', methods=['POST'])
  def create_actor():
    body = request.get_json()  
    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)
    new_movies = body.get('movies', None)

    movie_list = []

    for movie in new_movies:
      new = Movie.query.filter(Movie.name==movie).first()
      # if len(new) = 0:
      #   abort
      movie_list.append(new)
    
    try:
      entry = Actor(name=new_name, age=new_age, gender=new_gender, \
                    movies=movie_list)
      entry.insert()

      return jsonify({
        'success': True, 
        'created': entry.id,
        'total_actors': len(Actor.query.all())
      })

    except Exception as ex:
      print(ex)
      return 'issue'

    
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)    