import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Actor,Movie
import os

casting_assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN')
casting_director_token = os.environ.get('CASTING_DIRECTOR_TOKEN')
executive_producer_token = os.environ.get('EXECUTIVE_PRODUCER_TOKEN')

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        DATABASE_URL_TEST = os.environ.get('DATABASE_URL_TEST')
        self.database_path = DATABASE_URL_TEST
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })
        self.client = self.app.test_client

        self.new_actor = {
        "name": "Test Person",
        "age": "42",
        "gender": "Male"
        }
        self.new_movie = {
        "title": "Test Movie",
        "release_date": "2024-08-15",
        "genre": "Action"
        }

        # Define headers for different roles
        self.assistant_headers = {
            'Authorization': f'Bearer {casting_assistant_token}'
        }
        self.director_headers = {
            'Authorization': f'Bearer {casting_director_token}'
        }
        self.executive_headers = {
            'Authorization': f'Bearer {executive_producer_token}'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            # Add a sample actor and movie to be used in tests
            sample_actor = Actor(
                name=self.new_actor["name"],
                age=self.new_actor["age"],
                gender=self.new_actor["gender"]
            )
            sample_movie = Movie(
                title=self.new_movie["title"],
                release_date=self.new_movie["release_date"],
                genre=self.new_movie["genre"]
            )
            self.db.session.add(sample_actor)
            self.db.session.add(sample_movie)
            self.db.session.commit()

            self.sample_actor_id = sample_actor.id  # Store the ID only
            self.sample_movie_id = sample_movie.id  # Store the ID only


    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_get_main(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["message"], 'Casting Agency Website - this page requires no authentication')

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_get_actors_fail(self):
        res = self.client().get('/actors1234568', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_get_movies_fail(self):
        res = self.client().get('/movies1234568', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

   
    def test_add_actors(self):
        res = self.client().post('/actors', headers=self.director_headers, json={
        "name": "Test Person",
        "age": "42",
        "gender": "Male"
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data)
        

    def test_add_actors_fail(self):
        res = self.client().post('/actors',headers=self.director_headers, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_update_actors(self):
        updated_actor = {
            "name": "Updated Person",
            "age": "30",
            "gender": "Female"
        }
        res = self.client().patch(f'/actors/{self.sample_actor_id}',headers=self.director_headers, json=updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_update_actors_fail(self):
        res = self.client().patch('/actors/123456789',headers=self.director_headers, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
       
    def test_delete_actors(self):
        res = self.client().delete(f'/actors/{self.sample_actor_id}',headers=self.director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], self.sample_actor_id)

    def test_delete_actors_fail(self):
        res = self.client().delete('/actors/123456789',headers=self.director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_add_movies(self):
        res = self.client().post('/movies',headers=self.executive_headers, json={
            "title": "Test Movie",
            "release_date": "2024-08-15",
            "genre": "Action"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data)

    def test_add_movies_fail(self):
        res = self.client().post('/movies',headers=self.executive_headers, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_update_movies(self):
        updated_movie = {
            "title": "Updated Movie",
            "release_date": "2025-01-01",
            "genre": "Drama",
        }
        res = self.client().patch(f'/movies/{self.sample_movie_id}',headers=self.director_headers, json=updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_update_movies_fail(self):
        res = self.client().patch('/movies/123456789',headers=self.director_headers, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_movies(self):
        res = self.client().delete(f'/movies/{self.sample_movie_id}',headers=self.executive_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], self.sample_movie_id)

        # Check if the movie is deleted from the database
        movie = Movie.query.filter_by(id=self.sample_movie_id).one_or_none()
        self.assertIsNone(movie)

    def test_delete_movies_fail(self):
        res = self.client().delete('/movies/123456789',headers=self.executive_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_404_error_handler(self):
        response = self.client().get('/nonexistent_route',headers=self.director_headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_422_error_handler(self):
        response = self.client().post('/movies',headers=self.executive_headers, json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')

    def post_movie_as_assistant_fail(self):
        res = self.client().post('/movies',headers=self.assistant_headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def post_movie_as_director_fail(self):
        res = self.client().post('/movies',headers=self.director_headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()