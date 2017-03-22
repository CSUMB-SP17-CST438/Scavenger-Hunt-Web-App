import os
import flask
import flask_socketio
import requests
import flask_sqlalchemy
from flask import request
from urlparse import urlparse
import re
import imghdr
import requests_oauthlib
import json
import random


app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

import models 


ip = [];
all_chats = [];
all_online_users = [];
all_possible_online_users = [];
food = []
imageType = ["png", "PNG", "jpg", "JPG", "jpeg", "JPEG", "gif", "GIF"]
imgType = ["image/jpeg", "image/png", "image/gif"]
chatBotImg = 'https://lh4.googleusercontent.com/vnCZbUminSYgNXsQdiQffUnjXa0XMnIS0_rqkynkjZb5_dM8jVfvAN68MuCRRCC4HYYMxXgp=s50-h50-e365'
# chatBotImg = 'http://a.deviantart.net/avatars/s/a/sandara.jpg'
    
@app.route('/')
def hello():
    return flask.render_template('index.html')
    


@socketio.on('connect')
def on_connect():
    print "SOMEONE CONNECTED"
    
    chats = models.Message.query.all()
    del all_chats[:]
    for user in chats:
        all_chats.append({        
            'name': user.user,        
            'picture': user.img,        
            'chat': user.chat, 
            'fbID': user.fbID,
            'url': user.url,
        })
    socketio.emit('allchats', { 
        'chats': all_chats,
        
    }, broadcast=True)
    
    users = models.Users.query.all()
    del all_online_users[:]
    for user in users:
        all_online_users.append({        
            'name': user.user,        
            'picture': user.img, 
            'media': user.media,
            'fbID': user.fbID,   
        })
    socketio.emit('allusers', { 
        'users': all_online_users,
        'onlineNum': len(all_online_users),
    }, broadcast=True)


@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'
    
    # print request.sid
    users = models.Users.query.all()
    
    # for u in users:
    #     if u.ip == request.sid:
            
    #         print u.user + " disconnected"
    #         print u.fbID;
    # print "DISCONNECTED: " + request.sid
        
    
@socketio.on('new chat google')
def on_new_chat_google(data):
    response = requests.get( 
    'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + data['google_user_token'])    
    json = response.json()
    
    posURL = urlparse(data['chat']) 
    
    if data['chat'].find("!!", 0, 2) != -1:
        if data['chat'].find("!! say", 0, 6) != -1:
            botChat = data['chat'][7:]
        elif data['chat'].find("!! food", 0, 7) != -1:
            foodMsg = data['chat'][8:]
            food = foodMsg.split(' ', 1)
            foodName = food[0]
            foodLoc = food[1]
            url = "https://api.yelp.com/v2/search?term="+foodName+"&location="+foodLoc+"&limit=40" 
            # oauth = requests_oauthlib.OAuth1(
            #     'P9HpnKvg3flN6o1KrsHgxw', 
            #     'uJm6epI8CUT968OQc_8K0xBR9PQ',
            #     'eCEh6_yEE7S1i0r3h7GNO-CIF_llaDOb',
            #     'V_SBhCGKhBruxND3mswQC1pYCYE'
            # )
            oauth = requests_oauthlib.OAuth1(
                os.getenv("YELP_CONSUMER_KEY"), 
                os.getenv("YELP_CONSUMER_SECRET_KEY"),
                os.getenv("YELP_TOKEN_KEY"),
                os.getenv("YELP_TOKEN_SECRET_KEY")
            )
            response = requests.get(url, auth=oauth)
            json_body = response.json()
            randNum = random.randint(0, 39) #only 40 hits are returned
            name = json_body["businesses"][randNum]["name"]
            yelpURL = json_body["businesses"][randNum]["url"]
            phone = json_body["businesses"][randNum]["display_phone"]
            foodStreet = json_body["businesses"][randNum]["location"]["display_address"][0]
            foodCity = json_body["businesses"][randNum]["location"]["display_address"][1]
            botChat = yelpURL
            all_chats.append({        
                'name': 'Dragon-bot',        
                'picture': chatBotImg,        
                'chat': botChat,   
                'url': 'U',
            })
            msg = models.Message(chatBotImg, '1', 'Dragon-bot', botChat, 'U')
            models.db.session.add(msg)
            models.db.session.commit()
            botChat = name + " " + foodStreet + " " + foodCity + " " + phone
            if not food:
                del food[:]
        else:
            if data['chat'] == "!! about":
                botChat = "Hello! I am Dragon-bot. This is a fun place to chat."
            elif data['chat'] == "!! help":
                botChat = "!! about \n!! help \n!! say \n!! rawr \n!! eat \n!! food sushi Monterey, CA"
            elif data['chat'] == "!! rawr":
                botChat = "RAAAAWR!!!"
            elif data['chat'] == "!! food":
                botChat = "coming soon"
            elif data['chat'] == "!! eat":
                botChat = "FREE FOOD! Thank you!"
            else:
                botChat = "Nope! Check out !! help"
        all_chats.append({        
            'name': 'Dragon-bot',        
            'picture': chatBotImg,        
            'chat': botChat,   
            'url': '',
        })
        msg = models.Message(chatBotImg, '1', 'Dragon-bot', botChat, '')
        models.db.session.add(msg)
        models.db.session.commit()
    elif posURL.scheme or posURL.netloc:
        image = requests.head(data['chat'])
        posImg = image.headers.get('content-type')
        if (posImg == "image/gif" or posImg == "image/png" or posImg == "image/jpeg"):
            all_chats.append({        
                'name': json['name'],        
                'picture': json['picture'],        
                'chat':  data['chat'], 
                'url': 'I',
            })
            msg = models.Message(json['picture'], data['gID'], json['name'], data['chat'], 'I')
            models.db.session.add(msg)
            models.db.session.commit()
        else:
            all_chats.append({        
                'name': json['name'],        
                'picture': json['picture'],        
                'chat':  data['chat'], 
                'url': 'U',
            })
            msg = models.Message(json['picture'], data['gID'], json['name'], data['chat'], 'U')
            models.db.session.add(msg)
            models.db.session.commit()
    else:
        all_chats.append({        
        'name': json['name'],        
        'picture': json['picture'],        
        'chat': data['chat'],   
        'url': '',
        })
        msg = models.Message(json['picture'], data['gID'], json['name'], data['chat'], '')
        models.db.session.add(msg)
        models.db.session.commit()
    socketio.emit('all chats', { 
        'chats': all_chats,
    }, broadcast=True)
    
    print "Got an event for new google with data:", data    





@socketio.on('new chat')
def on_new_chat(data):
    response = requests.get( 
        'https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + data['facebook_user_token'])    
    json = response.json()
    
    posURL = urlparse(data['chat'])  
        
    
    if data['chat'].find("!!", 0, 2) != -1:
        if data['chat'].find("!! say", 0, 6) != -1:
            botChat = data['chat'][7:]
        elif data['chat'].find("!! food", 0, 7) != -1:
            foodMsg = data['chat'][8:]
            food = foodMsg.split(' ', 1)
            foodName = food[0]
            foodLoc = food[1]
            url = "https://api.yelp.com/v2/search?term="+foodName+"&location="+foodLoc+"&limit=40" 
            # oauth = requests_oauthlib.OAuth1(
            #     'P9HpnKvg3flN6o1KrsHgxw', 
            #     'uJm6epI8CUT968OQc_8K0xBR9PQ',
            #     'eCEh6_yEE7S1i0r3h7GNO-CIF_llaDOb',
            #     'V_SBhCGKhBruxND3mswQC1pYCYE'
            # )
            oauth = requests_oauthlib.OAuth1(
                os.getenv("YELP_CONSUMER_KEY"), 
                os.getenv("YELP_CONSUMER_SECRET_KEY"),
                os.getenv("YELP_TOKEN_KEY"),
                os.getenv("YELP_TOKEN_SECRET_KEY")
            )
            response = requests.get(url, auth=oauth)
            json_body = response.json()
            randNum = random.randint(0, 39) #only 40 hits are returned
            name = json_body["businesses"][randNum]["name"]
            yelpURL = json_body["businesses"][randNum]["url"]
            phone = json_body["businesses"][randNum]["display_phone"]
            foodStreet = json_body["businesses"][randNum]["location"]["display_address"][0]
            foodCity = json_body["businesses"][randNum]["location"]["display_address"][1]
            botChat = yelpURL
            all_chats.append({        
                'name': 'Dragon-bot',        
                'picture': chatBotImg,        
                'chat': botChat,   
                'url': 'U',
            })
            msg = models.Message(chatBotImg, '1', 'Dragon-bot', botChat, 'U')
            models.db.session.add(msg)
            models.db.session.commit()
            botChat = name + " " + foodStreet + " " + foodCity + " " + phone
            if not food:
                del food[:]
        else:
            if data['chat'] == "!! about":
                botChat = "Hello! I am Dragon-bot. This is a fun place to chat."
            elif data['chat'] == "!! help":
                botChat = "!! about \n!! help \n!! say \n!! rawr \n!! eat \n!! food sushi Monterey, CA"
            elif data['chat'] == "!! rawr":
                botChat = "RAAAAWR!!!"
            elif data['chat'] == "!! eat":
                botChat = "FREE FOOD! Thank you!"
            else:
                botChat = "Nope! Check out !! help"
        all_chats.append({        
            'name': 'Dragon-bot',        
            'picture': chatBotImg,        
            'chat': botChat,   
            'url': '',
        })
        msg = models.Message(chatBotImg, '1', 'Dragon-bot', botChat, '')
        models.db.session.add(msg)
        models.db.session.commit()
    elif posURL.scheme or posURL.netloc:
        image = requests.head(data['chat'])
        posImg = image.headers.get('content-type')
        if (posImg == "image/gif" or posImg == "image/png" or posImg == "image/jpeg"):
            all_chats.append({        
                'name': json['name'],        
                'picture': json['picture']['data']['url'],        
                'chat':  data['chat'], 
                'url': 'I',
            })
            msg = models.Message(json['picture']['data']['url'], json['id'], json['name'], data['chat'], 'I')
            models.db.session.add(msg)
            models.db.session.commit()
        else:
            all_chats.append({        
                'name': json['name'],        
                'picture': json['picture']['data']['url'],        
                'chat':  data['chat'], 
                'url': 'U',
            })
            msg = models.Message(json['picture']['data']['url'], json['id'], json['name'], data['chat'], 'U')
            models.db.session.add(msg)
            models.db.session.commit()
    else:
        all_chats.append({        
        'name': json['name'],        
        'picture': json['picture']['data']['url'],        
        'chat': data['chat'],
        'url': '',
        })
        msg = models.Message(json['picture']['data']['url'], json['id'], json['name'], data['chat'], '')
        models.db.session.add(msg)
        models.db.session.commit()
    socketio.emit('all chats', { 
        'chats': all_chats,
    }, broadcast=True)
    
    print "Got an event for new number with data:", data
    
    
@socketio.on('fbConnected')
def fbConnection(data):
    response = requests.get( 
    'https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + data['facebook_user_token'])    
    json = response.json()
    flag = False;
    
    
    botChat = 'Welcome, ' + json['name'] + '! Say hi, everyone!!!'
    all_chats.append({        
        'name': 'Dragon-bot',        
        'picture': chatBotImg,        
        'chat': botChat,  
        'url': '',
    })
    msg = models.Message(chatBotImg, '1', 'Dragon-bot', botChat, '')
    models.db.session.add(msg)
    models.db.session.commit()
    
    socketio.emit('all chats', { 
        'chats': all_chats,
    }, broadcast=True)
    
    
    users = models.Users.query.all()
    del all_online_users[:]
    for user in users:
        all_online_users.append({        
            'name': user.user,        
            'picture': user.img,   
            'media': user.media,
            'fbID': user.fbID,   
        })
    
    
    for user in users:
        if (user.user == json['name']):
            flag = True;
    if (flag == False):
        all_online_users.append({
                'name': json['name'],        
                'picture': json['picture']['data']['url'],
                'media': 'FB',
            })
        usr = models.Users(json['picture']['data']['url'], json['id'], 'FB', json['name'], request.sid)
        models.db.session.add(usr)
        models.db.session.commit()
    socketio.emit('fbConn', { 
        'users': all_online_users,
        'onlineNum': len(all_online_users),
        }, broadcast=True)
        

@socketio.on('gConnect')
def gConnection(data):
    response = requests.get( 
    'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + data['google_user_token'])    
    json = response.json()
    
    
    botChat = 'Welcome, ' + json['name'] + '! Say hi, everyone!!!'
    all_chats.append({        
        'name': 'Dragon-bot',        
        'picture': chatBotImg,        
        'chat': botChat,  
        'url': '',
    })
    msg = models.Message(chatBotImg, '1', 'Dragon-bot', botChat, '')
    models.db.session.add(msg)
    models.db.session.commit()
    
    socketio.emit('all chats', { 
        'chats': all_chats,
    }, broadcast=True)
    
    users = models.Users.query.all()
    del all_online_users[:]
    for user in users:
        all_online_users.append({        
            'name': user.user,        
            'picture': user.img,
            'media': user.media,
            'fbID': user.fbID,   
        })
        
    flag = False;
    for user in users:
        if (user.user == json['name']):
            flag = True;
    if (flag == False):
        all_online_users.append({
                'name': json['name'],        
                'picture': json['picture'],
                'media': 'G'
            })
        usr = models.Users(json['picture'], data['gID'], 'G', json['name'], request.sid)
        models.db.session.add(usr)
        models.db.session.commit()
        
        socketio.emit('gConn', { 
        'users': all_online_users,
        'onlineNum': len(all_online_users),
        }, broadcast=True)
    
  
    
# @socketio.on('gLoggedIn')
# def gLog(data):
#     print " GOOOOOOGLE"
#     print data['gUser']
    
        
@socketio.on('fbDisconnected')
def fbDisconnection(data):
    offlineUser = models.Users.query.filter_by(fbID=data['userID']).first();
    discUser = offlineUser.user;
    models.db.session.delete(offlineUser)
    models.db.session.commit()
    
    
    users = models.Users.query.all()
    del all_online_users[:]
    for user in users:
        all_online_users.append({        
            'name': user.user,        
            'picture': user.img,  
            'media': user.media,
            'fbID': user.fbID,   
        })
    
    socketio.emit('allusers', { 
        'users': all_online_users,
        'onlineNum': len(all_online_users),
    }, broadcast=True)
    
    botChat = 'Aww! ' + discUser + ' left us...'
    all_chats.append({        
        'name': 'Dragon-bot',        
        'picture': chatBotImg,        
        'chat': botChat, 
        'url': '',
    })
    msg = models.Message(chatBotImg, '1', 'Dragon-bot', botChat, '')
    models.db.session.add(msg)
    models.db.session.commit()
    
    socketio.emit('all chats', { 
        'chats': all_chats,
    }, broadcast=True)
    
 

@socketio.on('gDisconnected')
def gDisconnection(data):
    offlineUser = models.Users.query.filter_by(fbID=data['userID']).first();
    discUser = offlineUser.user;
    models.db.session.delete(offlineUser)
    models.db.session.commit()
    
    
    users = models.Users.query.all()
    del all_online_users[:]
    for user in users:
        all_online_users.append({        
            'name': user.user,        
            'picture': user.img, 
            'media': user.media,
            'fbID': user.fbID,   
        })
    
    socketio.emit('allusers', { 
        'users': all_online_users,
        'onlineNum': len(all_online_users),
    }, broadcast=True)
    
    botChat = 'Aww! ' + discUser + ' left us...'
    all_chats.append({        
        'name': 'Dragon-bot',        
        'picture': chatBotImg,        
        'chat': botChat,   
        'url': '',
    })
    msg = models.Message(chatBotImg, '1', 'Dragon-bot', botChat, '')
    models.db.session.add(msg)
    models.db.session.commit()
    
    socketio.emit('all chats', { 
        'chats': all_chats,
    }, broadcast=True)
    
    

if __name__ == '__main__':  # __name__!
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
