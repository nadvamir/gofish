# gofish

This is a project to test information foraging theory, disguised as a fishing game. You can build many different decision based games using the engine provided. The engine will log user actions, which can later be analysed for trends.

## API reference

The game engine interfaces with the world via a pseudo REST API:

* `GET /gofish/api/v2/home/` -- Level list

  Returns a list of levels that are in the game. Response:
  
  ```javascript
  {'levels': {
    'id'       : int,    // level id
    'name'     : string, // display name of the level
    'unlocked' : bool,   // whether the level has been unlocked
    'active'   : bool,   // whether the level can be unlocked
    'cost'     : int,    // how much does it cost to unlock this level
    'stars'    : int,    // personal high score rating out of 3
    'highS'    : int,    // personal high score
    'maxHighS' : int    // global high score
  }}
  ```

* `GET /gofish/api/v2/player/` -- Player info

  Details about player. Response:
  
  ```javascript
 {'player': {
    'money' : int,    // how much money the player has
    'boat'  : int,    // index of the player's boat in the upgrade list. -1 if none
    'line'  : int,    // index of the player's line in the upgrade list. -1 if none
    'cue'   : int,    // index of the player's cues in the upgrade list. -1 if none
    'lineN' : string, // name of the players line
    'cueN'  : string  // name of the players cues
  }}
  ```
* `GET /gofish/api/v2/shop/` -- Upgrades a player can buy

* `GET /gofish/api/v2/trophies/` -- Trophies list

* `GET /gofish/api/v2/game/` -- Game instance if one exists

* `GET /gofish/api/start/:levelID/` -- Start new game

* `GET /gofish/api/end/` -- End the current game

* `GET /gofish/api/action/move/left/` -- Move left on the map

* `GET /gofish/api/action/move/right/` -- Move right on the map

* `GET /gofish/api/action/inspect/:N/` -- List of potential catches

  Get a list of stuff you'd catch if you fished in the current location :N times

* `GET /gofish/api/action/catchnonil/:listOfSuccess/` -- Catch specified fish, Nil yields skipped

* `GET /gofish/api/action/carchall/:listOfSuccess/` -- Catch specified fish or nothing, without any skipping

* `GET /gofish/api/update/:target/` -- Upgrade given category (boat, cues, etc.)

* `GET /gofish/api/buy/:bait/` -- Buy given bait

* `GET /gofish/api/choose/:bait/` -- Choose to use given bait in fishing

* `GET /gofish/api/getmodifiers/` -- List of baits

* Deprecated. `GET /gofish/api/getgame/` -- Returns all relevant game info at once

* Deprecated. `GET /gofish/api/getupdates/` -- List of upgrades you can buy

## Modifying the code

## Optimising the game

## Analysing data

## Etc.

Link to the work plan:
https://docs.google.com/spreadsheets/d/1rHUUuBQpQ0nNazDMxY83rYowcEJzyMJdz9iQSwqf90E/edit?usp=sharing

Link to the deployed version:
http://nadvamir.pythonanywhere.com/gofish/
