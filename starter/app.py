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

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  def delete_movie(movie_id):
    try:
      #Later, add feature to warn user about deleting permanently
      movie = Movie.query.get(movie_id).one_or_none()
      movie.actors = []
      db.session.commit()

      if movie is None:
        print('error')
        #abort(404)

      movie.delete()


      return jsonify({
        'success': True,
        'deleted': movie_id,
        'total_movies': len(Movie.query.all())
      })
      
    except Exception as ex:
      print(ex)
      return 'issue'     

  @app.route('/movies/<int:movie_id>', methods=['PATCH']) 
  def edit_movie(movie_id):
    body = request.get_json()  
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if movie is None:
        print('error')
        #abort(404)

      if 'name' in body:
        movie.name = body.get('name')
      if 'actors' in body:  
        movie.actors = body.get('actors')
      if 'release_date' in body:
        movie.release_date = int(body.get('release_date'))
      movie.update()

      return jsonify({
        'success': True,
        'edited': movie_id,
        'total_movies': len(Movie.query.all())
      })
      
    except Exception as ex:
      print(ex)
      #abort(400)
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

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  def delete_actor(actor_id):
    try:
      #Later, add feature to warn user about deleting permanently
      actor = Actor.query.get(actor_id)
      actor.movies = []
      db.session.commit()

      if actor is None:
        print('error')
        #abort(404)

      actor.delete()


      return jsonify({
        'success': True,
        'deleted': actor_id,
        'total_movies': len(Actor.query.all())
      })
      
    except Exception as ex:
      print(ex)
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  def edit_actor(actor_id):
    body = request.get_json()  
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if actor is None:
        print('error')
        #abort(404)

      if 'name' in body:
        actor.name = body.get('name', None)
      if 'movies' in body:
        actor.movies = body.get('movies')
      if 'age' in body:
        actor.age = int(body.get('age'))
      actor.update()

      return jsonify({
        'success': True,
        'edited': actor_id,
        'total_actors': len(Actor.query.all())
      })
      
    except Exception as ex:
      print(ex)
      #abort(400)
      return 'issue'
      
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)    