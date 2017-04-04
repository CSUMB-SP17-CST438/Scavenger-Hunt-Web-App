import os
import flask
import flask_socketio
import requests
import flask_sqlalchemy
from flask import request
import requests_oauthlib
import json
import random
import math 
import urllib2



def location_lookup():
    try:
        return json.load(urllib2.urlopen('http://ipinfo.io/json'))
    except urllib2.HTTPError:
        return False

location = location_lookup()

# print city and latitude/longitude
print location['city'] + ' (' + location['loc'] + ')'



app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

# import models 

    
@app.route('/')
def hello():
    return flask.render_template('index.html')
    


@socketio.on('connect')
def on_connect():
    print "SOMEONE CONNECTED"
    


@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'
    
@socketio.on('location')
def on_location():
    print "grabbed location"
    
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))   
    

    
    

if __name__ == '__main__':  # __name__!
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

def chestRadius(user_lat, user_lon, chest_lat,chest_lon):
    radius_number = 35 #here where are we going to change the value for which the 
    total_lat = user_lat - chest_lat
    total_lon = user_lon - chest_lon
    
    total_col = math.sqrt((total_lat * total_lat) + (total_lon * total_lon))
    
    if total_col < radius_number:
        print "You are in the chest area."
        return True
    
