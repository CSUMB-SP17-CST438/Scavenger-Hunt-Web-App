# models.py
import flask_sqlalchemy,app
import os

app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://proj2_user:project2handin1@localhost/postgres'  
db = flask_sqlalchemy.SQLAlchemy(app.app)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    img = db.Column(db.String(150))
    fbID = db.Column(db.String(150))
    user = db.Column(db.String(120))
    chat = db.Column(db.Text)
    url = db.Column(db.String(5))
    def __init__(self, i, f, u, c, ur):
        self.img = i
        self.fbID = f
        self.user = u
        self.chat = c
        self.url = ur
    def __repr__(self): # what's __repr__?
        return '<Message chat: %s>' % self.chat

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    img = db.Column(db.String(150))
    fbID = db.Column(db.String(150))
    media = db.Column(db.String(50))
    user = db.Column(db.String(120))
    ip = db.Column(db.String(120))
    def __init__(self, i, f, m, u, p):
        self.img = i
        self.fbID = f
        self.media = m
        self.user = u
        self.ip = p
    def __repr__(self): # what's __repr__?
        return '<Users name: %s>' % self.user
        
class ipAddr(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    ip = db.Column(db.String(120))
    def __init__(self, p):
        self.ip = p
    def __repr__(self): # what's __repr__?
        return '<ipAddr ip: %s>' % self.ip