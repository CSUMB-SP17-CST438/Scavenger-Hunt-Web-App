import os
import flask
import flask_socketio
import requests
import flask_sqlalchemy
from flask import request
import requests_oauthlib
import json
import random

import models

import bearing
import points

chestsCoords = []


app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

# import models 

lat = 0.0
lng = 0.0

parkLat = 0.0
parkLng = 0.0

movingValue = 0.000065

def setCoords(x, y):
    global lat
    global lng
    lat = x
    lng = y
    
def getLat():
    return lat
    
def getLng():
    return lng
    
def setDemoCoords(x, y):
    global latDemo
    global lngDemo
    latDemo = x
    lngDemo = y
    
def getDemoLat():
    return latDemo
    
def getDemoLng():
    return lngDemo
    
def setParkCoords(x, y):
    global parkLat
    global parkLng
    parkLat = x
    parkLng = y
    
def getParkLat():
    return parkLat
    
def getParkLng():
    return parkLng
    
def setCurrChestLat(x):
    global chestLatitude
    chestLatitude = x
    
def setCurrChestLng(x):
    global chestLongitude
    chestLongitude = x

def getCurrChestLat():
    return chestLatitude
    
def getCurrChestLng():
    return chestLongitude
    
def setChestNum(x):
    global chestNum
    chestNum = x
    
def getChestNum():
    return chestNum
    
def setObtainedKey(x):
    global key
    key = x
    
def getObtainedKey():
    return key
    
    
@app.route('/')
def hello():
    return flask.render_template('index.html')
    
@app.route('/demo')
def demo():
    return flask.render_template('demo.html')

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
    # print getLat()
    # print getLng()
    # hint()
    # findNearestPark()
    # sendPark()
    
@socketio.on('startDemo')
def start_game_demo(data):
    setDemoCoords(data['coords']['lat'], data['coords']['lng'])
    findNearestPark()
    sendPark()
    createChests()
    createDoor()
    showDoorOnMap()
    setChestNum(1)
    x,y = chestsCoords[0]
    setCurrChestLat(x)
    setCurrChestLng(y)
    hint()
    print getDemoLat()
    print getDemoLng()
    
@socketio.on('start')
def start_game(data):
    if (lat != 0 and lng != 0):
        findNearestPark()
        sendPark()
        createChests()
        createDoor()
        showDoorOnMap()
        setChestNum(1)
        x,y = chestsCoords[0]
        setCurrChestLat(x)
        setCurrChestLng(y)
        hint()
        
    else:
        print "location not shared"
        
@socketio.on('updateLocation')
def update_player(data):
    setCoords(data['coords']['lat'], data['coords']['lng'])
    print "update"
    print data['coords']['lat']
    print data['coords']['lng']
    if (getObtainedKey() == 'Y'):
        checkDistance(getDoorLat(), getDoorLng())
    else:
        checkDistance(getCurrChestLat(), getCurrChestLng())
    
@socketio.on('my event')
def handle_my_custom_event(data):
    print('received data: ' + data['test'])   
    
@socketio.on('test')
def testing(data):
    print data['testVar']['lat']
    print data['testVar']['lng']
    

def hint():
    # updateChestStatus()
    
    bAngle = bearing.bearing(getLat(), getLng(), getCurrChestLat(), getCurrChestLng())
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
    
    
def updateChestStatus():
    # global chest1
    # global chest2
    # global chest3
    # global chest4
    # global chest5
    # retrieve from database
    if (getChestNum() == 1):
        setChestNum(2)
        x,y = chestsCoords[1]
        setCurrChestLat(x)
        setCurrChestLng(y)
        setObtainedKey('N')
    elif (getChestNum() == 2):
        setChestNum(3)
        x,y = chestsCoords[2]
        setCurrChestLat(x)
        setCurrChestLng(y)
        setObtainedKey('N')
    elif (getChestNum() == 3):
        setChestNum(4)
        x,y = chestsCoords[3]
        setCurrChestLat(x)
        setCurrChestLng(y)
        setObtainedKey('N')
    elif (getChestNum() == 4):
        setChestNum(5)
        x,y = chestsCoords[4]
        setCurrChestLat(x)
        setCurrChestLng(y)
    elif (getChestNum() == 5):
        setObtainedKey('Y')
        unlockDoor()
    # if (chest1 == 'Y' and chest2 == 'N'):
    #     x,y = chestsCoords[0]
    #     setCurrChestLat(x)
    #     setCurrChestLng(y)
    # elif (chest2 == 'Y' and chest3 == 'N'):
    #     x,y = chestsCoords[1]
    #     setCurrChestLat(x)
    #     setCurrChestLng(y)
    # elif (chest3 == 'Y' and chest4 == 'N'):
    #     x,y = chestsCoords[2]
    #     setCurrChestLat(x)
    #     setCurrChestLng(y)
    # elif (chest4 == 'Y' and chest5 == 'N'):
    #     x,y = chestsCoords[3]
    #     setCurrChestLat(x)
    #     setCurrChestLng(y)
    # elif (chest5 == 'Y'):
    #     x,y = chestsCoords[4]
    #     setCurrChestLat(x)
    #     setCurrChestLng(y)
    # chest1 = 'Y'
    # chest2 = 'N'
    # chest3 = 'N'
    # chest4 = 'N'
    # chest5 = 'N'
    
def checkDistance(lat, lng):
    if (getObtainedKey() == 'Y'):
        if (bearing.haversine(lat, lng, getLat(), getLng()) < 3):
            print "at door"
            # congrats
        else:
            print "not at door"
            
    else:
        if (bearing.haversine(lat, lng, getLat(), getLng()) < 3):
            print "found it"
            # update db
            updateChestStatus()
            
        else:
            hint()
        
def unlockDoor():
    socketio.emit('hideUpdateButton', {
        
    });
    
def findNearestPark():
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(getLat())+","+str(getLng())+"&radius=804&types=park&key=AIzaSyBs4cGYz3h3Zx5ZDi8oaAtHsobIkXQvQOs"
    response = requests.get(url)
    json_body = response.json()
    # print json_body["results"][0]["geometry"]["location"]["lat"]
    # print json_body["results"][0]["geometry"]["location"]["lng"]
    # print json_body
    setParkCoords(json_body["results"][0]["geometry"]["location"]["lat"], json_body["results"][0]["geometry"]["location"]["lng"])
    print "park coords"
    print getParkLat()
    print getParkLng()
    
def sendPark():
    socketio.emit('parkLoc', {
      'parkCoordsLat': getParkLat(),
      'parkCoordsLng': getParkLng(),
    });
    socketio.emit('hideStartButton', {
        
    });
    
@socketio.on('up')
def move_up(data):
    goUp(getDemoLat(), getDemoLng())
    
def createChests():
    for i in range(0,5):
        # print i
        chestsCoords.append(points.create_random_point(getParkLat(),getParkLng(), 100))
    
def createDoor():
    x,y = points.create_random_point(getParkLat(),getParkLng(), 100)
    setDoorLat(x)
    setDoorLng(y)
    
def setDoorLat(x):
    global doorLat
    doorLat = x
    
def setDoorLng(y):
    global doorLng
    doorLng = y
    
def getDoorLat():
    return doorLat

def getDoorLng():
    return doorLng
    
    
def showDoorOnMap():
    x = getDoorLat()
    y = getDoorLng()
    socketio.emit('door', {
      'doorLat': x,
      'doorLng': y,
    });
    
def goUp(x,y):
    latDemo = x + movingValue
    print latDemo
    setDemoCoords(latDemo, getDemoLng())
    print "demo"
    socketio.emit('playerLoc', {
       'demoLat': getDemoLat(),
       'demoLng': getDemoLng(),
    });
    print getDemoLat()
    
def goDown(x,y):
    down = x - movingValue
    
def goRight(x,y):
    right = y  + movingValue
    
def goLeft(x,y):
    left = y - movingValue

if __name__ == '__main__':  # __name__!
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
