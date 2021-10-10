from sqlalchemy import Column, String, Integer, DateTime,ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()
migrate = Migrate()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app,db)


'''
Actors
Have title and release year
'''
class Actors(db.Model):  
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(500), nullable=False)
    lastname = Column(String(500),nullable=False)
    gender = Column(String(100))
    age =  Column(Integer) 
    relation = db.relationship('Relations',backref='actors',lazy='joined',cascade='all,delete')

    def __init__(self, firstname, lastname,gender,age):
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age
    
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
        'firstname': self.firstname,
        'lastname': self.lastname,
        'gender': self.gender,
        'age': self.age}


class Movies(db.Model):
    __tablename__ = 'movies'    
     
    id = Column(Integer, primary_key=True)
    title = Column(String(500),nullable=False, unique= True)
    release_date = Column(String(100))
    relation = db.relationship('Relations',backref='movies',lazy='joined',cascade='all,delete')
    
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def format(self):
        return{
        'id': self.id,
        'title':self.title,
        'release_date':self.release_date}

class Relations(db.Model):
    __tablename__ = 'relations'
    
    id = Column(Integer,primary_key=True)
    movie_id = Column(Integer,ForeignKey('movies.id'),nullable=False)
    actor_id = Column(Integer,ForeignKey('actors.id'),nullable=False)
    
    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def format(self):
        return{
        'id': self.id,
        'movie_id':self.movie_id,
        'actor_id':self.actor_id}
    
    