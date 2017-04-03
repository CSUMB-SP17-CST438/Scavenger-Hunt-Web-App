import os
import flask
import flask_socketio
import requests
import flask_sqlalchemy
from flask import request
import requests_oauthlib
import json
import random

import bearing



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
    hint()
    
@socketio.on('my event')
def handle_my_custom_event(data):
    print('received data: ' + data['test'])   
    
@socketio.on('test')
def testing(data):
    print data['testVar']['lat']
    print data['testVar']['lng']
    

def hint():
    bAngle = bearing.bearing(getLat(), getLng(), 36.654179, -121.798798)
    if (bAngle > 0 and bAngle < 22.5) or (bAngle > 337.5 and bAngle < 360):
        # up arrow
        arrow = 'up'
    elif (bAngle > 22.5 and bAngle <= 67.5):
        # ne arrow
        arrow = 'ne'
    elif (bAngle > 67.5 and bAngle <= 112.5):
        # right arrow
        arrow = 'right'
    elif (bAngle > 112.5 and bAngle <= 157.5):
        # se arrow
        arrow = 'se'
    elif (bAngle > 157.5 and bAngle <= 202.5):
        #  down arrow
        arrow = 'down'
    elif (bAngle > 202.5 and bAngle <= 247.5):
        # sw arrow
        arrow = 'sw'
    elif (bAngle > 247.5 and bAngle <= 292.5):
        # left arrow
        arrow = 'left'
    elif (bAngle > 292.5 and bAngle <= 337.5):
        # nw arrow
        arrow = 'nw'
    socketio.emit('arrow', {
        'arrowDir': arrow
    })
    
    

if __name__ == '__main__':  # __name__!
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
