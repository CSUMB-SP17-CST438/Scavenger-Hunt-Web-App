# models.py
import flask_sqlalchemy
# import app
import os


# app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')exit
db = flask_sqlalchemy.SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    img = db.Column(db.String(500))
    fbID = db.Column(db.String(500))
    user = db.Column(db.String(150))
    def __init__(self, i, f, u):
        self.img = i
        self.fbID = f
        self.user = u
    def __repr__(self): # what's __repr__?
        return '<Users name: %s>' % self.user

class chestInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    user = db.Column(db.String(150))
    chestNumber = db.Column(db.Integer)
    coordinates = db.Column(db.String(150))
    status = db.Column(db.String(100))
    fbID = db.Column(db.String(500))
    def __init__(self, u, c, xy, s,f):
        self.user = u
        self.chestNumber = c
        self.coordinates = xy
        self.status = s
        self.fbID = f
    def __repr__(self): # what's __repr__?
        return '<Users Chest: %s>' % self.user  
        
class doorInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    user = db.Column(db.String(150))
    coordinates = db.Column(db.String(150))
    statusLocked = db.Column(db.String(100))
    fbID = db.Column(db.String(500))
    def __init__(self, u, xy, s,f):
        self.user = u
        self.coordinates = xy
        self.statusLocked = s
        self.fbID = f
    def __repr__(self): # what's __repr__?
        return '<Users Chest: %s>' % self.user 

class progress(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    user = db.Column(db.String(150))
    gameSession = db.Column(db.String(100))
    parkName = db.Column(db.String(150))
    fbID = db.Column(db.String(500))
    start = db.Column(db.String(150))
    end = db.Column(db.String(150))

    def __init__(self, u, g,p,f,s,e):
        self.user = u
        self.gameSession = g
        self.parkName = p
        self.fbID = f
        self.start = s
        self.end = e
    def __repr__(self): # what's __repr__? I still dont have a clue 
        return '<User Progress: %s>' % self.user 