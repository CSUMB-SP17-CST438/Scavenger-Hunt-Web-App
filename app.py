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
import bearing
import points
import datetime
from decimal import *
import time

import models


app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://proj3_user:project3@localhost/postgres'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)
models.db.init_app(app)

all_users = [];
chestsCoords = []

lat = 0.0
lng = 0.0

parkLat = 0.0
parkLng = 0.0

movingValue = 0.000065

def setFBid(x):
    global fbID
    fbID = x
    
def getFBid():
    return fbID

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
    
def setParkName(x):
    global parkName
    parkName = x
    
def getParkName():
    return parkName
    
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
    
def getCurrChestCoords():
    return (chestLatitude, chestLongitude)
    
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
    
@app.route('/keyquest')
def landing_page():
    return flask.render_template('key.html')

@socketio.on('connect')
def on_connect():
    print "SOMEONE CONNECTED"
    
@socketio.on('fbConnect')
def on_fbConnect(data):
    response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + data['facebook_user_token'])    
    json = response.json()
    if (data['facebook_user_token'] != ''):
        print "Fb connect"
        print json['name']
        setFBid(json['id'])
        print json['id']
        print getFBid()
        print "fb id above"
        userProg = models.progress.query.filter_by(fbID=getFBid()).first();
        print userProg
        if (userProg.gameSession == 'Y'):
            print "yes"
            if (latDemo != 0 and lngDemo != 0):
                print "location"
                socketio.emit('playerLoc', {
                   'demoLat': getDemoLat(),
                   'demoLng': getDemoLng(),
                });
                setParkName(userProg.parkName)
                print getParkName()
                print "testing fb"
                # x,y = userProg.
                # setParkCoords(json_body["results"][0]["geometry"]["location"]["lat"], json_body["results"][0]["geometry"]["location"]["lng"])
              
    else:
        print "not fb connect"

@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'
    
@socketio.on('geolocation')
def on_location(data):
    # lat = data['coords']['lat']
    # lng = data['coords']['lng']
    setCoords(data['coords']['lat'], data['coords']['lng'])
    setDemoCoords(data['coords']['lat'], data['coords']['lng'])
    print getDemoLat()
    print getDemoLng()
    # hint()
    # findNearestPark()
    # sendPark()
    
@socketio.on('startDemo')
def start_game_demo(data):
    del chestsCoords[:]
    # users = models.Users.query.all()
    users = models.db.session.query(models.Users).all()
    
    # # print "Test"
    if (latDemo != 0 and lngDemo != 0):
        response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + data['facebook_user_token'])    
        json = response.json()
        flag = False;
        print json['name']
        
        setFBid(json['id'])
        
        
            # print "added TO DATABASe!"
        socketio.emit('playerLoc', {
           'demoLat': getDemoLat(),
           'demoLng': getDemoLng(),
        });
        # findNearestPark(getDemoLat(), getDemoLng())
        # sendPark()
        # createChests()
        # showChestOnMap()
        # createDoor()
        # setObtainedKey('N')
        # showDoorOnMap()
        # setChestNum(1)
        # x,y = chestsCoords[0]
        # setCurrChestLat(x)
        # setCurrChestLng(y)
        # hint(getDemoLat(), getDemoLng())
        # print getDemoLat()
        # print getDemoLng()
        
        del all_users[:]
        for user in users:
            all_users.append({        
                'name': user.user,        
                'picture': user.img, 
                'fbID': user.fbID,   
            })
        
        
        for user in users:
            if (user.user == json['name']):
                print "already started"
                prk = models.parkInfo.query.filter_by(fbID=json['id']).first();
                setParkName(prk.parkName)
                # print "park coords"
                # print prk.coordinates
                pX, pY = prk.coordinates.strip('()').split(',')
                pX = float(pX)
                pY = float(pY)
                # pX = float(prk.coordinates[1:11])
                # pY = float(prk.coordinates[12:24])
                setParkCoords(pX, pY)
                sendPark()
                chst = models.chestInfo.query.filter_by(fbID=json['id']).all();
                dr = models.doorInfo.query.filter_by(fbID=json['id']).first();
                for c in chst:
                    # print "chests"
                    # print c.coordinates
                    # tempX = Decimal(c.coordinates[1:19])
                    # tempY = Decimal(c.coordinates[20:39])
                    tempX, tempY = c.coordinates.strip('()').split(',')
                    tempX = float(tempX)
                    tempY = float(tempY)
                    tempCoord = tempX, tempY
                    chestsCoords.append(tempCoord)
                for c in chst:
                    # print "chest status"
                    # print c.status
                    if (c.status == 'Y'):
                        # print "yes"
                        # print c.chestNumber
                        if (c.chestNumber == 1):
                            socketio.emit('changeChest1', {
        
                            });
                        elif (c.chestNumber == 2):
                            socketio.emit('changeChest2', {
        
                            });
                        elif (c.chestNumber == 3):
                            socketio.emit('changeChest3', {
        
                            });
                        elif (c.chestNumber == 4):
                            socketio.emit('changeChest4', {
        
                            });
                        elif (c.chestNumber == 5):
                            socketio.emit('changeChest5', {
        
                            });
                            if (dr.statusLocked == 'Y'):
                                setObtainedKey('Y')
                                print "yes to the key"
                for c in chst:
                    if (c.status == 'N'):
                        # cX = Decimal(c.coordinates[1:19])
                        # cY = Decimal(c.coordinates[20:39])
                        cX, cY = c.coordinates.strip('()').split(',')
                        cX = float(cX)
                        cY = float(cY)
                        # cX, cY = c.coordinates
                        setChestNum(c.chestNumber)
                        # if (c.chestNumber != 5):
                        #     setObtainedKey('N')
                        setCurrChestLat(cX)
                        setCurrChestLng(cY)
                        setObtainedKey('N')
                        hint(getDemoLat(), getDemoLng())
                        break
                    # elif (c.chestNumber == 5 and dr.statusLocked == 'Y'):
                    #     setObtainedKey('Y')
                    #     print "yes to the key"
                showChestOnMap()
                dX, dY = dr.coordinates.strip('()').split(',')
                dX = float(dX)
                dY = float(dY)
                setDoorLat(dX)
                setDoorLng(dY)
                showDoorOnMap()
                
                
                flag = True;
        if (flag == False):
            findNearestPark(getDemoLat(), getDemoLng())
            sendPark()
            createChests()
            showChestOnMap()
            createDoor()
            setObtainedKey('N')
            showDoorOnMap()
            setChestNum(1)
            x,y = chestsCoords[0]
            setCurrChestLat(x)
            setCurrChestLng(y)
            hint(getDemoLat(), getDemoLng())
            all_users.append({
                    'name': json['name'],        
                    'picture': json['picture']['data']['url'],
                    'media': 'FB',
                })
    # users = models.db.session.query(models.Users).all()
            usr = models.Users(json['picture']['data']['url'], json['id'], json['name'])
            models.db.session.add(usr)
            models.db.session.commit()
            
            park = models.progress(json['name'], 'Y', json['id'], str(datetime.datetime.now()).split('.')[0], '')
            models.db.session.add(park)
            models.db.session.commit()
            
            chest = models.chestInfo(json['name'], 1, chestsCoords[0], 'N', json['id'])
            models.db.session.add(chest)
            models.db.session.commit()
            chest = models.chestInfo(json['name'], 2, chestsCoords[1], 'N', json['id'])
            models.db.session.add(chest)
            models.db.session.commit()
            chest = models.chestInfo(json['name'], 3, chestsCoords[2], 'N', json['id'])
            models.db.session.add(chest)
            models.db.session.commit()
            chest = models.chestInfo(json['name'], 4, chestsCoords[3], 'N', json['id'])
            models.db.session.add(chest)
            models.db.session.commit()
            chest = models.chestInfo(json['name'], 5, chestsCoords[4], 'N', json['id'])
            models.db.session.add(chest)
            models.db.session.commit()
            
            door = models.doorInfo(json['name'], (getDoorLat(), getDoorLng()), 'Y', json['id'])
            models.db.session.add(door)
            models.db.session.commit()
            
            park = models.parkInfo(json['name'], getParkName(), (getParkLat(), getParkLng()), json['id'])
            models.db.session.add(park)
            models.db.session.commit()
        
        
    else:
        print "location not shared"
    
@socketio.on('start')
def start_game(data):
    del chestsCoords[:]
    # users = models.Users.query.all()
    users = models.db.session.query(models.Users).all()
    
    # # print "Test"
    if (latDemo != 0 and lngDemo != 0):
        response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + data['facebook_user_token'])    
        json = response.json()
        flag = False;
        print json['name']
        
        setFBid(json['id'])
        
        socketio.emit('playerLoc', {
        'lat': getLat(),
        'lng': getLng(),
        })
        
        for user in users:
            if (user.user == json['name']):
                print "already started"
                prk = models.parkInfo.query.filter_by(fbID=json['id']).first();
                setParkName(prk.parkName)
                # print "park coords"
                # print prk.coordinates
                pX, pY = prk.coordinates.strip('()').split(',')
                pX = float(pX)
                pY = float(pY)
                # pX = float(prk.coordinates[1:11])
                # pY = float(prk.coordinates[12:24])
                setParkCoords(pX, pY)
                sendPark()
                chst = models.chestInfo.query.filter_by(fbID=json['id']).all();
                dr = models.doorInfo.query.filter_by(fbID=json['id']).first();
                for c in chst:
                    # print "chests"
                    # print c.coordinates
                    # tempX = Decimal(c.coordinates[1:19])
                    # tempY = Decimal(c.coordinates[20:39])
                    tempX, tempY = c.coordinates.strip('()').split(',')
                    tempX = float(tempX)
                    tempY = float(tempY)
                    tempCoord = tempX, tempY
                    chestsCoords.append(tempCoord)
                for c in chst:
                    # print "chest status"
                    # print c.status
                    if (c.status == 'Y'):
                        # print "yes"
                        # print c.chestNumber
                        if (c.chestNumber == 1):
                            socketio.emit('changeChest1', {
        
                            });
                        elif (c.chestNumber == 2):
                            socketio.emit('changeChest2', {
        
                            });
                        elif (c.chestNumber == 3):
                            socketio.emit('changeChest3', {
        
                            });
                        elif (c.chestNumber == 4):
                            socketio.emit('changeChest4', {
        
                            });
                        elif (c.chestNumber == 5):
                            socketio.emit('changeChest5', {
        
                            });
                            if (dr.statusLocked == 'Y'):
                                setObtainedKey('Y')
                                print "yes to the key"
                for c in chst:
                    if (c.status == 'N'):
                        # cX = Decimal(c.coordinates[1:19])
                        # cY = Decimal(c.coordinates[20:39])
                        cX, cY = c.coordinates.strip('()').split(',')
                        cX = float(cX)
                        cY = float(cY)
                        # cX, cY = c.coordinates
                        setChestNum(c.chestNumber)
                        # if (c.chestNumber != 5):
                        #     setObtainedKey('N')
                        setCurrChestLat(cX)
                        setCurrChestLng(cY)
                        setObtainedKey('N')
                        hint(getDemoLat(), getDemoLng())
                        break
                    # elif (c.chestNumber == 5 and dr.statusLocked == 'Y'):
                    #     setObtainedKey('Y')
                    #     print "yes to the key"
                showChestOnMap()
                dX, dY = dr.coordinates.strip('()').split(',')
                dX = float(dX)
                dY = float(dY)
                setDoorLat(dX)
                setDoorLng(dY)
                showDoorOnMap()
                
                
                flag = True;
        if (flag == False):
            findNearestPark(getLat(), getLng())
            sendPark()
            createChests()
            showChestOnMap()
            createDoor()
            setObtainedKey('N')
            showDoorOnMap()
            setChestNum(1)
            x,y = chestsCoords[0]
            setCurrChestLat(x)
            setCurrChestLng(y)
            hint(getLat(), getLng())
            
            all_users.append({
                    'name': json['name'],        
                    'picture': json['picture']['data']['url'],
                    'media': 'FB',
                })
    # users = models.db.session.query(models.Users).all()
            usr = models.Users(json['picture']['data']['url'], json['id'], json['name'])
            models.db.session.add(usr)
            models.db.session.commit()
            
            park = models.progress(json['name'], 'Y', json['id'], str(datetime.datetime.now()).split('.')[0], '')
            models.db.session.add(park)
            models.db.session.commit()
            
            chest = models.chestInfo(json['name'], 1, chestsCoords[0], 'N', json['id'])
            models.db.session.add(chest)
            models.db.session.commit()
            chest = models.chestInfo(json['name'], 2, chestsCoords[1], 'N', json['id'])
            models.db.session.add(chest)
            models.db.session.commit()
            chest = models.chestInfo(json['name'], 3, chestsCoords[2], 'N', json['id'])
            models.db.session.add(chest)
            models.db.session.commit()
            chest = models.chestInfo(json['name'], 4, chestsCoords[3], 'N', json['id'])
            models.db.session.add(chest)
            models.db.session.commit()
            chest = models.chestInfo(json['name'], 5, chestsCoords[4], 'N', json['id'])
            models.db.session.add(chest)
            models.db.session.commit()
            
            door = models.doorInfo(json['name'], (getDoorLat(), getDoorLng()), 'Y', json['id'])
            models.db.session.add(door)
            models.db.session.commit()
            
            park = models.parkInfo(json['name'], getParkName(), (getParkLat(), getParkLng()), json['id'])
            models.db.session.add(park)
            models.db.session.commit()
        
    else:
        print "location not shared"
        
@socketio.on('updateDemoLocation')
def update_player_demo(data):
    print "update demo"
    if (getObtainedKey() == 'Y'):
        checkDistance(getDoorLat(), getDoorLng(), getDemoLat(), getDemoLng())
    else:
        checkDistance(getCurrChestLat(), getCurrChestLng(), getDemoLat(), getDemoLng())
        
@socketio.on('updateLocation')
def update_player(data):
    print "UPDATE LOCATION"
    setCoords(data['coords']['lat'], data['coords']['lng'])
    socketio.emit('playerLoc', {
        'lat': getLat(),
        'lng': getLng(),
        })
    # print "update"
    # print data['coords']['lat']
    # print data['coords']['lng']
    if (getObtainedKey() == 'Y'):
        checkDistance(getDoorLat(), getDoorLng(), getLat(), getLng())
    else:
        checkDistance(getCurrChestLat(), getCurrChestLng(), getLat(), getLng())
    
@socketio.on('my event')
def handle_my_custom_event(data):
    print('received data: ' + data['test'])   
    
@socketio.on('test')
def testing(data):
    print data['testVar']['lat']
    print data['testVar']['lng']
    
    

def hint(playerLat, playerLng):
    # updateChestStatus()
    
    bAngle = bearing.bearing(playerLat, playerLng, getCurrChestLat(), getCurrChestLng())
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
        socketio.emit('changeIcon1', {
        
        });
    #print"changed"
        setChestNum(2)
        x,y = chestsCoords[1]
        setCurrChestLat(x)
        setCurrChestLng(y)
        setObtainedKey('N')
        # models.progress.query.filter_by(fbID=getFBid()).first();
        updateChest = models.chestInfo.query.filter_by(fbID=getFBid()).filter_by(chestNumber=1).first()
        # print updateChest
        # print "chest updated ^"
        updateChest.status = 'Y'
        models.db.session.commit()
    elif (getChestNum() == 2):
        socketio.emit('changeIcon2', {
        
        });
        setChestNum(3)
        x,y = chestsCoords[2]
        setCurrChestLat(x)
        setCurrChestLng(y)
        setObtainedKey('N')
        updateChest = models.chestInfo.query.filter_by(fbID=getFBid()).filter_by(chestNumber=2).first()
        # print updateChest
        # print "chest updated ^"
        updateChest.status = 'Y'
        models.db.session.commit()
    elif (getChestNum() == 3):
        socketio.emit('changeIcon3', {
        
        });
        setChestNum(4)
        x,y = chestsCoords[3]
        setCurrChestLat(x)
        setCurrChestLng(y)
        setObtainedKey('N')
        updateChest = models.chestInfo.query.filter_by(fbID=getFBid()).filter_by(chestNumber=3).first()
        # print updateChest
        # print "chest updated ^"
        updateChest.status = 'Y'
        models.db.session.commit()
    elif (getChestNum() == 4):
        socketio.emit('changeIcon4', {
        
        });
        setChestNum(5)
        x,y = chestsCoords[4]
        setCurrChestLat(x)
        setCurrChestLng(y)
        updateChest = models.chestInfo.query.filter_by(fbID=getFBid()).filter_by(chestNumber=4).first()
        # print updateChest
        # print "chest updated ^"
        updateChest.status = 'Y'
        models.db.session.commit()
    elif (getChestNum() == 5):
        socketio.emit('changeIcon5', {
        
        });
        x,y = getDoorCoords()
        setCurrChestLat(x)
        setCurrChestLng(y)
        
        setObtainedKey('Y')
        updateChest = models.chestInfo.query.filter_by(fbID=getFBid()).filter_by(chestNumber=5).first()
        # print updateChest
        # print "chest updated ^"
        updateChest.status = 'Y'
        models.db.session.commit()
        unlockDoor()
        print "no arrow"
        arrow = ''
        socketio.emit('arrow', {
            'arrowDir': arrow
        })
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
    
def checkDistance(itemLat, itemLng, playerLat, playerLng):
    if (getObtainedKey() == 'Y'):
        if (bearing.haversine(itemLat, itemLng, playerLat, playerLng) < 2):
            print "at door"
            print "yay"
            # congrats
            socketio.emit('youwin',{
                
            });
            updateDoor = models.doorInfo.query.filter_by(fbID=getFBid()).first()
            # print updateDoor
            # print "door updated ^"
            updateDoor.statusLocked = 'N'
            models.db.session.commit()
            prog = models.progress.query.filter_by(fbID=getFBid()).first()
            prog.end = str(datetime.datetime.now()).split('.')[0]
            models.db.session.commit()
            postToFacebook()
            deleteData()
        else:
            hint(playerLat, playerLng)
    else:
        if (bearing.haversine(itemLat, itemLng, playerLat, playerLng) < 1):
            print "found it"
            # update db
            updateChestStatus()
            hint(playerLat, playerLng)
            
        else:
            hint(playerLat, playerLng)
            
def postToFacebook():
    print "posted"
    prog = models.progress.query.filter_by(fbID=getFBid()).first()
    start = prog.start
    end = prog.end
    
    print start
    
    fmt = '%Y-%m-%d %H:%M:%S'
    d1 = datetime.datetime.strptime(start, fmt)
    d2 = datetime.datetime.strptime(end, fmt)
    
    d1_ts = time.mktime(d1.timetuple())
    d2_ts = time.mktime(d2.timetuple())

    totalMin = int(d2_ts-d1_ts) / 60
    print "total min"
    print totalMin
    
def deleteData():
    print "deleted from db"
    usr = models.Users.query.filter_by(fbID=getFBid()).first();
    models.db.session.delete(usr)
    models.db.session.commit()
    
    prg = models.progress.query.filter_by(fbID=getFBid()).first();
    models.db.session.delete(prg)
    models.db.session.commit()
    
    prk = models.parkInfo.query.filter_by(fbID=getFBid()).first();
    models.db.session.delete(prk)
    models.db.session.commit()
    
    chst = models.chestInfo.query.filter_by(fbID=getFBid()).filter_by(chestNumber=1).first();
    models.db.session.delete(chst)
    models.db.session.commit()
    chst = models.chestInfo.query.filter_by(fbID=getFBid()).filter_by(chestNumber=2).first();
    models.db.session.delete(chst)
    models.db.session.commit()
    chst = models.chestInfo.query.filter_by(fbID=getFBid()).filter_by(chestNumber=3).first();
    models.db.session.delete(chst)
    models.db.session.commit()
    chst = models.chestInfo.query.filter_by(fbID=getFBid()).filter_by(chestNumber=4).first();
    models.db.session.delete(chst)
    models.db.session.commit()
    chst = models.chestInfo.query.filter_by(fbID=getFBid()).filter_by(chestNumber=5).first();
    models.db.session.delete(chst)
    models.db.session.commit()
    
    dr = models.doorInfo.query.filter_by(fbID=getFBid()).first();
    models.db.session.delete(dr)
    models.db.session.commit()
    
    socketio.emit('restart', {
        
    });
    socketio.emit('resetting', {
        
    })
        
def unlockDoor():
    socketio.emit('showKeyButton', {
        
    });
    
def findNearestPark(playerLat, playerLng):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(playerLat)+","+str(playerLng)+"&radius=804&types=park&key=AIzaSyBs4cGYz3h3Zx5ZDi8oaAtHsobIkXQvQOs"
    response = requests.get(url)
    json_body = response.json()
    # print json_body["results"][0]["geometry"]["location"]["lat"]
    # print json_body["results"][0]["geometry"]["location"]["lng"]
    # print "park name"
    # print json_body["results"][0]["name"]
    setParkName(json_body["results"][0]["name"])
    # print json_body
    setParkCoords(json_body["results"][0]["geometry"]["location"]["lat"], json_body["results"][0]["geometry"]["location"]["lng"])
    # print "park coords"
    # print getParkLat()
    # print getParkLng()
    
def sendPark():
    socketio.emit('parkLoc', {
      'parkCoordsLat': getParkLat(),
      'parkCoordsLng': getParkLng(),
    });
    socketio.emit('parkArea', {
      'parkLat': getParkLat(),
      'parkLng': getParkLng(),
    });
    socketio.emit('hideStartButton', {
        
    });
    # socketio.emit('showParkCirlce', {
        
    # });
    
@socketio.on('up')
def move_up(data):
    goUp(getDemoLat(), getDemoLng())
    
@socketio.on('down')
def move_down(data):
    goDown(getDemoLat(), getDemoLng())
    
@socketio.on('right')
def move_right(data):
    goRight(getDemoLat(), getDemoLng())
    
@socketio.on('left')
def move_left(data):
    goLeft(getDemoLat(), getDemoLng())
    
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
    
def getDoorCoords():
    return (getDoorLat(), getDoorLng())
    
    
def showDoorOnMap():
    x = getDoorLat()
    y = getDoorLng()
    socketio.emit('door', {
      'doorLat': x,
      'doorLng': y,
    });
    
def showChestOnMap():
    for i in chestsCoords:
        x, y = i
        # print "hello"
        socketio.emit('chests', {
          'chestLat': x,
          'chestLng': y,
        });
    
def goUp(x,y):
    latDemo = x + movingValue
    # print latDemo
    setDemoCoords(latDemo, getDemoLng())
    # print "demo"
    socketio.emit('playerLoc', {
       'demoLat': getDemoLat(),
       'demoLng': getDemoLng(),
    });
    # print getDemoLat()
    
def goDown(x,y):
    # print x
    latDemo = x - movingValue
    # print "demo"
    # print latDemo
    setDemoCoords(latDemo, getDemoLng())
    # print getDemoLat()
    socketio.emit('playerLoc', {
       'demoLat': getDemoLat(),
       'demoLng': getDemoLng(),
    });
    
def goRight(x,y):
    lngDemo = y  + movingValue
    setDemoCoords(getDemoLat(), lngDemo)
    socketio.emit('playerLoc', {
       'demoLat': getDemoLat(),
       'demoLng': getDemoLng(),
    });
    
def goLeft(x,y):
    lngDemo = y - movingValue
    setDemoCoords(getDemoLat(), lngDemo)
    socketio.emit('playerLoc', {
       'demoLat': getDemoLat(),
       'demoLng': getDemoLng(),
    });

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
    
