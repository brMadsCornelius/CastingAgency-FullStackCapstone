import os
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
from settings import DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD

# setting up the environment variables so we dont have to write it in terminal every time
os.environ["FLASK_APP"] = "flaskr"
os.environ["FLASK_ENV"] = "development"

database_path = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:5432/{DATABASE_NAME}"

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def setup_migrations(app):
    migrate = Migrate(app,db)
    

"""
Actor model

"""
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
            }
    

"""
Movie model

"""
class Movie(db.model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    genre = Column(String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return({
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "genre": self.genre
        })