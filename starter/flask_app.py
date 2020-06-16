import os
from flask import Flask, request, abort, jsonify, redirect, url_for, \
    render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
# from auth import *

# https://dev-l0ayxsy2.auth0.com/authorize?audience=CA&response_type=token
# &client_id=qnY6u1FIxnfHYX1nBFjCskAsxPrRc2EC&
# redirect_uri=http://127.0.0.1:3000/

ITEMS_PER_PAGE = 15

def paginate_items(request, selection, type):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [type.format() for type in selection]
    current_items = items[start: end]
    return current_items


app = Flask(__name__)
app.config.from_object('config.TestConfig')
database_name = 'casting'
database_path = 'postgresql://{}:{}@{}/{}'.format(
                    'postgres', 1, 'localhost:5432', database_name)
setup_db(app, database_path=database_path)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, DELETE')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all')
# @requires_auth('get:movies', 'get:actors')
def get_all():
    selection = Movie.query.order_by(Movie.id).all()
    current_movies = paginate_items(request, selection, Movie)
    if (len(current_movies) == 0):
        abort(404)

    actor_selection = Actor.query.order_by(Actor.id).all()
    current_actors = paginate_items(request, actor_selection, Actor)
    if (len(current_actors) == 0):
        abort(404)

    return render_template('success.html', data=current_movies,
        actors=current_actors)        

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
# @requires_auth('delete:movie')
def delete_movie(movie_id):
    # Later, add feature to warn user about deleting permanently
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    movie.actors = []
    db.session.commit()

    if movie is None:
        # print('error')
        abort(404)

    movie.delete()

    return jsonify({
                    'success': True,
                    'deleted': movie_id
    })     

@app.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    actor.movies = []
    db.session.commit()

    if actor is None:
        # print('error')
        abort(404)

    actor.delete()

    return jsonify({
                    'success': True,
                    'deleted': actor_id,
                    'total_actors': len(Actor.query.all())
    })

@app.route('/new_movie')
def view_movie_form():
    actors = Actor.query.order_by(Actor.id).all()
    return render_template('new_movie.html', actors=actors)
@app.route('/new_movie', methods=['POST'])
def create_movie():
    body = request.get_json()
    new_name = body.get('name', None)
    new_release = body.get('release_date', None)
    new_actors = body.get('actors', None)
    actor_list = []

    for actor in new_actors:
        formatted = Actor.query.get(actor)
        actor_list.append(formatted)

    try:
        entry = Movie(name=new_name, release_date=new_release,
                        actors=actor_list)
        entry.insert()

        return jsonify({
            'success': True,
            'created': entry.id,
            'total_movies': len(Movie.query.all())
        })    
    except Exception as ex:
        # print(ex) 
        return jsonify({'success': False})   

@app.route('/new_actor')
def view_actor_form():
    movies = Movie.query.order_by(Movie.id).all()
    return render_template('new_actor.html', movies=movies)

@app.route('/new_actor', methods=['POST'])
def create_actor():
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    movies = body.get('movies', None)
    movie_list = []

    for movie in movies:
        formatted = Movie.query.get(movie)
        movie_list.append(formatted)

    print(movie_list)
    try:
        entry = Actor(name=name, age=age, gender=gender, movies=movie_list)
        entry.insert()

        return jsonify({
            'success': True,
            'created': entry.id,
            'total_actors': len(Actor.query.all())
        })    
    except Exception as ex:
        # print(ex) 
        return jsonify({'success': False})       