import os
import flask
import flask_socketio
import requests
import flask_sqlalchemy
from flask import request
import requests_oauthlib
import json
import random



app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

# import models 

lat = 0.0
lng = 0.0

def setCoords(x, y):
    global lat
    global lng
    lat = x
    lng = y
    
def getLat():
    return lat
    
def getLng():
    return lng
    
@app.route('/')
def hello():
    return flask.render_template('index.html')
    


@socketio.on('connect')
def on_connect():
    print "SOMEONE CONNECTED"
    


@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'
    
@socketio.on('geolocation')
def on_location(data):
    # lat = data['coords']['lat']
    # lng = data['coords']['lng']
    setCoords(data['coords']['lat'], data['coords']['lng'])
    print getLat()
    print getLng()
    
@socketio.on('my event')
def handle_my_custom_event(data):
    print('received data: ' + data['test'])   
    
@socketio.on('test')
def testing(data):
    print data['testVar']['lat']
    print data['testVar']['lng']
    

    
    

if __name__ == '__main__':  # __name__!
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
