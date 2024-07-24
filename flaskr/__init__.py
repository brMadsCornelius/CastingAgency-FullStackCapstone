from flask import Flask, request, abort, jsonify
from models import Actor,Movie,setup_db,setup_migrations
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
        setup_migrations(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
    CORS(app)

    @app.route('/')
    def main():
        return 'Casting Agency test123'
    return app