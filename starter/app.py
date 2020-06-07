import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  # @app.after_request
  # def after_request(response):
  #     response.headers.add('Access-Control-Allow-Headers',
  #                           'Content-Type, Authorization')
  #     response.headers.add('Access-Control-Allow-Methods',
  #                           'GET, POST, DELETE')
  #     response.headers.add('Access-Control-Allow-Credentials', 'true')
  #     return response

  # @app.route('/')

  @app.route('/actors')
  def get_actors():
    names = []
    for actor in Actor.query.all():
      names.append(actor.name)
    return jsonify({'actors': names})

  @app.route('/movies')
  def get_movies():
    names = []
    for movie in Movie.query.all():
      names.append(movie.name)
    return jsonify({'movies': names})
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)    