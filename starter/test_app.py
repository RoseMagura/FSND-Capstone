import os
from dotenv import load_dotenv
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import create_app
from models import db, setup_db, Movie, Actor


load_dotenv()

assistant_token = os.getenv('assistant_token')
director_token = os.getenv('director_token')
exec_token = os.getenv('exec_token')
assistant_header = {
        'Authorization': f'Bearer {assistant_token}'
    }
director_header = {
    'Authorization': f'Bearer {director_token}'}

exec_header = {
    'Authorization': f'Bearer {exec_token}'}


class CastingTestCase(unittest.TestCase):
    '''This class represents the casting test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        # self.app = create_app()
        self.app = create_app()
        self.client = self.app.test_client
        database_name = 'casting_test'
        database_username = 'postgres:1'
        self.database_path = 'postgres://{}@{}/{}'.format(
            database_username, 'localhost:5432', database_name)
        setup_db(self.app, self.database_path)

        # Create a new entry with fake data to test posting movie
        self.new_movie = {
            'name': 'c',
            'release_date': 2003,
            'actors': ['b']
        }

        # Create a new entry with fake data to test posting actor
        self.new_actor = {
                'name': 'b',
                'age': 45,
                'gender': 'female',
                'movies': ['c']
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy(self.app)
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        '''Executed after reach test'''
        pass

    def test_get_paginated_movies(self):
        res = self.client().get('/movies', headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_404_sent_requesting_beyond_valid_movie_page(self):
        res = self.client().get('/movies?page=500', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_paginated_actors(self):
        res = self.client().get('/actors', headers=exec_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_beyond_valid_actor_page(self):
        res = self.client().get('/actors?page=500', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/8', headers=exec_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 8).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 8)
        self.assertTrue(data['total_movies'])
        self.assertEqual(movie, None)

    def test_delete_movie_without_permission(self):
        res = self.client().delete('/movies/8', headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers=exec_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_movie(self):
        res = self.client().post('/movies', headers=exec_header,
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_new_movie_without_permission(self):
        res = self.client().post('/movies', headers=director_header,
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_405_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies/1', headers=exec_header,
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_edit_movie(self):
        res = self.client().patch('/movies/4', headers=exec_header,
                                  json={'name': 'The Matrix',
                                        'release_date': 1999,
                                        'actors': ['b']})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['edited'], 4)

    def test_422_if_movie_does_not_exist_patch(self):
        res = self.client().patch('/movies/1000', headers=exec_header,
                                  json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_edit_actor(self):
        res = self.client().patch('/actors/1', headers=exec_header,
                                  json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['edited'], 1)

    def test_422_if_actor_does_not_exist(self):
        res = self.client().patch('/actors/1000', headers=exec_header,
                                  json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_actor(self):
        res = self.client().post('/actors', headers=exec_header,
                                 json={
                                    'name': 'Baka',
                                    'age': 20,
                                    'gender': 'male',
                                    'movies': ['Bad Bakas']
                                        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors/1', headers=exec_header,
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_create_new_actor_without_permission(self):
        res = self.client().post('/actors', headers=assistant_header,
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_edit_movie_without_permission(self):
        res = self.client().patch('/movies/4', headers=assistant_header,
                                  json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_delete_actor(self):
        res = self.client().delete('/actors/5', headers=exec_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertTrue(data['total_actors'])
        self.assertEqual(actor, None)

    def test_delete_actor_without_permission(self):
        res = self.client().delete('/actors/1', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_422_if_actor_does_not_exist_delete(self):
        res = self.client().delete('/actors/1000', headers=exec_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
