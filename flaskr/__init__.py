from flask import Flask, request, abort, jsonify
from models import Actor,Movie,setup_db
from flask_cors import CORS
from datetime import datetime

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
    CORS(app)

    @app.route('/')
    def main():
        return 'Casting Agency Website'
    

    # Get Movies
    @app.route('/movies')
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()

        if len(movies) == 0:
            abort(404)

        # Format each actor
        formatted_movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formatted_movies
        })


    # Get Actors
    @app.route('/actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()

        if len(actors) == 0:
            abort(404)

        # Format each actor
        formatted_actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': formatted_actors
        })
        

    # Delete Actors
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        actor = Actor.query.get(actor_id)
        
        if actor is None:
            abort(404)
        
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'deleted': actor_id
            })
        except:
            abort(422)

    # Delete Movies
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        movie = Movie.query.get(movie_id)
        
        if movie is None:
            abort(404)
        
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'deleted': movie_id
            })
        except:
            abort(422)

    # POST Actors
    @app.route('/actors', methods=["POST"])
    def add_actors():
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
     
        # Ensuer that input has data
        if new_name==None or new_age==None or new_gender==None:
            abort(422)

        try:
            actor = Actor(name=new_name,age=new_age,gender=new_gender)

            actor.insert()

            return jsonify({
                'success': True,
                'name':  actor.name,
                'age':  actor.age,
                'gender' : actor.gender 
            })
        except:
            abort(422)

    # POST Movies
    @app.route('/movies', methods=["POST"])
    def add_movies():
        body = request.get_json()

        new_title = body.get('title')
        new_release_date = body.get('release_date')
        new_genre = body.get('genre')
    
        # Ensure that input has data
        if not new_title or not new_release_date or not new_genre:
            abort(422)

        try:
            # Convert release_date from string to date
            release_date = datetime.strptime(new_release_date, '%Y-%m-%d').date()
            
            movie = Movie(title=new_title, release_date=release_date, genre=new_genre)
            movie.insert()

            return jsonify({
                'success': True,
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date.isoformat(),
                'genre': movie.genre
            })
        except:
            abort(422)

    # Patch Actors
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def patch_actor(actor_id):
        actor = Actor.query.get(actor_id)
        
        if actor is None:
            abort(404)

        body = request.get_json()
        
        # Extract updated values from request body
        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')
        
        # Update actor attributes if provided
        if new_name is not None:
            actor.name = new_name

        if new_age is not None:
            actor.age = new_age
            
        if new_gender is not None:
            actor.gender = new_gender

        try:
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except:
            abort(422)

    # Patch Movies
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def patch_movie(movie_id):
        movie = Movie.query.get(movie_id)
        
        if movie is None:
            abort(404)

        body = request.get_json()
        
        # Extract updated values from request body
        new_title = body.get('title')
        new_release_date = body.get('release_date')
        new_genre = body.get('genre')
        
        # Update movie attributes if provided
        if new_title is not None:
            movie.title = new_title

        if new_release_date is not None:
            # Convert release_date from string to date
            try:
                movie.release_date = datetime.strptime(new_release_date, '%Y-%m-%d').date()
            except ValueError:
                abort(422)  # Invalid date format

        if new_genre is not None:
            movie.genre = new_genre

        try:
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable"}),
            422,
        )

    return app