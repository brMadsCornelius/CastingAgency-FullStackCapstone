from flask import Flask, request, abort, jsonify
from models import Actor,Movie,setup_db
from flask_cors import CORS
from flask_migrate import Migrate,setup_migrations

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