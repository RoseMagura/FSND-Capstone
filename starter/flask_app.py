import os
from flask import Flask, request, abort, jsonify, redirect, url_for, \
    render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import *

# https://dev-l0ayxsy2.auth0.com/authorize?audience=CA&response_type=token
# &client_id=qnY6u1FIxnfHYX1nBFjCskAsxPrRc2EC&
# redirect_uri=http://127.0.0.1:3000/

ITEMS_PER_PAGE = 10

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

# @app.route('/')
# def index():
#     return 'Hello World'

@app.route('/')
# @requires_auth('get:movies')
def get_all():
    selection = Movie.query.order_by(Movie.id).all()
    M = []
    for s in selection:
        name = s.format()['name']
        M.append(name)
    current_movies = paginate_items(request, selection, Movie)

    if (len(current_movies) == 0):
        abort(404)

    # return jsonify({
    #     'success': True,
    #     'movies': current_movies,
    #     'total_movies': len(selection),
    #     })
# @requires_auth('get:movies')
    actor_selection = Actor.query.order_by(Actor.id).all()
    A = []
    for s in actor_selection:
        name = s.format()['name']
        A.append(name)
    # current_actors = paginate_items(request, selection, Actor)

    # if (len(current_actors) == 0):
    #     abort(404)

    # return jsonify({
    #     'success': True,
    #     'movies': current_movies,
    #     'total_movies': len(selection),
    #     })
    return render_template('success.html', data=M,
        actors=A)        