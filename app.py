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
import models



def location_lookup():
    try:
        return json.load(urllib2.urlopen('http://ipinfo.io/json'))
    except urllib2.HTTPError:
        return False

location = location_lookup()

# print city and latitude/longitude
print location['city'] + ' (' + location['loc'] + ')'

import bearing



app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

# import models 

lat = 0.0
lng = 0.0

parkLat = 0.0
parkLng = 0.0

def setCoords(x, y):
    global lat
    global lng
    lat = x
    lng = y
    
def getLat():
    return lat
    
def getLng():
    return lng
    
def setParkCoords(x, y):
    global parkLat
    global parkLng
    parkLat = x
    parkLng = y
    
def getParkLat():
    return parkLat
    
def getParkLng():
    return parkLng
    
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
    findNearestPark()
    sendPark()
    
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
    
    
def findNearestPark():
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(getLat())+","+str(getLng())+"&radius=804&types=park&key=AIzaSyBs4cGYz3h3Zx5ZDi8oaAtHsobIkXQvQOs"
    response = requests.get(url)
    json_body = response.json()
    print json_body["results"][0]["geometry"]["location"]["lat"]
    print json_body["results"][0]["geometry"]["location"]["lng"]
    print json_body
    setParkCoords(json_body["results"][0]["geometry"]["location"]["lat"], json_body["results"][0]["geometry"]["location"]["lng"])
    
    
def sendPark():
    socketio.emit('parkLoc', {
      'parkCoordsLat': getParkLat(),
      'parkCoordsLng': getParkLng(),
    });
    
def createChest():
    

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
    
