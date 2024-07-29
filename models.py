import os
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy

DATABASE_URL = os.environ.get('DATABASE_URL')
database_path = DATABASE_URL

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
    
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True  # So SQLAlchemy does not create a table for this model

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        raise NotImplementedError("Subclasses must implement this method")


class Actor(BaseModel):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Movie(BaseModel):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    genre = Column(String)

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "genre": self.genre
        }
