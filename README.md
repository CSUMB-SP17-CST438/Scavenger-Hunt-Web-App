# Scavenger-Hunt-Web-App

## What does our app do?
Players are able to locate their closest park to start looking for five treasure chests. They will be instructed to find these chests (one by one) by
the given direction pointer. Upon finding the last chest, they will be given a key. The key will unlock the locked door that is displayed on the map and
they will win the game.

Scavenger Hunt Web appication is the final group project for CST 438.
It combines technologies like Flask, Socketio, API calls, and React to 
display and interact with a map to find "chests" on the screen via park location.

## Who worked on it?
Samuel Valdez
Maria Loza

## What were you able to complete for this handin?
Everything that we were aiming and what it was lacking from handin 1.
The chests and door locations were created and stored. Grabbing the nearest park information. We also updated the database. The hint creator was completed, which
points to the location of the current chest based off its location and the player's location on the map. Implemented the key and the ability to unlock the door if
the player has the key.

## What are the known problems, if any, with your project?
If more than one device starts playing, their markers are shared throughout all the devices. We'll have to figure out how to make the web app personalized per 
person/device. 
This isn't really a problem. But we haven't been able to go out and test it out. But if we thought it out correctly, it should work.

## How would you improve it if you had more time?
Definitely, go outside and test it. 
Additionally, personalizing the web app.





## For the team ----------------------------------------------
Some starter code for React on Flask.

## Upgrade Node version to 6

```$ nvm install 6```

## Installing Webpack

```$ npm install -g webpack```

## Installing `npm` dependencies from `package.json`

```$ npm install```

## Compiling Javascript using Webpack

```$ webpack --watch```




