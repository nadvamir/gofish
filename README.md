# gofish

This is a project to test information foraging theory, disguised as a fishing game. You can build many different decision based games using the engine provided. The engine will log user actions, which can later be analysed for trends.

## Deployed version

[http://nadvamir.pythonanywhere.com/](http://nadvamir.pythonanywhere.com/)

## API reference

The game engine interfaces with the world via a pseudo REST API:

* `GET /gofish/api/v2/home/` -- Level list

  Returns a list of levels that are in the game. 
  
  Success response:
  
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

  Details about player. 
  
  Success response:
  
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
* `GET /gofish/api/v2/shop/` -- Upgrades the player can buy

  Returns a list of all upgrades in the game. 
  
  Success response:
  
  ```javascript
  {
    'boats' : [:update], // the list of boat upgrades
    'lines' : [:update], // the list of line upgrades
    'cues'  : [:update], // the list of cue upgrades
  }
  ```
  
  where `:update` is
  
  ```javascript
    {
      'name' : string, // the name of the upgrade
      'cost' : int,    // how much does it cost to upgrade to it
      'perk' : string  // a description of what this update does
    }
  ```
  
  Note, that while the entire list of upgrades is returned, the upgrade process is linear, 
  thus it is impossible to skip an upgrade. The entirety of upgrades are returned to allow
  a variety of visualisations for the shop screen.

* `GET /gofish/api/v2/trophies/` -- Trophies list

  Returns both the trophies that player has, as well as the best trophies in the whole game. 
  
  Success response:
  
  ```javascript
  {
    'userTrophies': [:trophy], // the list of trophies collected by the player
    'gameTrophies': [:trophy]  // the list of the best trophies in the game
  }
  ```
  Where `:trophy` is
  
  ```javascript
  {
      'name'   : string, // the name of the trophy
      'value'  : int,    // the value of the trophy in coins
      'weight' : float,  // the weight of the trophy
  }
  ```
  
* `GET /gofish/api/v2/game/` -- Game instance if one exists

  Returns the object for the game that the player is currently playing, or `404` if no games are played.
  
  Failure response:
  
  ```
  404 NOT FOUND
  ```
  
  Success response:
  
  ```javascript
  {'game' : {
    'level'     : int,     // level ID
    'day'       : int,     // how many games did the player played to date
    'name'      : string,  // the name of the level
    'totalTime' : int,     // total time there is in the game
    'timeLeft'  : int,     // how much time has left
    'valCaught' : int,     // the value of fish caught in this game
    'showDepth' : bool,    // whether showing the depth of the water is allowed
    'map'       : :map,    // the game map
    'position'  : int,     // the location the player is on the map
    'cues'      : :cues,   // game cues
    'caught'    : [:fish]  // the list of the fish caught in this game
  }}
  ```
  
  Where `:map` is
  
  ```javascript
  [[int, int, int...]] // the array of depths of fishing spots
                       // 2D array is a legacy
  ```
  
  and `:cues` are
  
  ```javascript
  [[:numberOfFish, :value]] // :numberOfFish -> int, -1 for not shown
                            // :value -> int, value indicator 0-4
  ```
  
  and `:fish` is
  
  ```javascript
  {
    'id'     : string, // fish type (bass, pike)
    'name'   : string, // display name (Bass, Pike)
    'weight' : float,  // weight of the fish in kg
    'length' : float,  // length of the fish in m
    'value'  : int,    // value of the fish in coins
  }
  ```

* `GET /gofish/api/start/:levelID/` -- Start new game

  Creates an instance of a new game. Will fail if the player is already in another game.
  
  Request parameters:
  
  ```javascript
  :levelID -> int // id of the level to isntantiate
  ```
  
  Failure response:
  
  ```javascript
  {
    'error': string // an unhelpful error message, not really displayable
  }
  ```
  
  With the introduction of API v2, the success response should be treated as `200 OK`. However, for the sake of completeness:
  
  ```javascript
  {
    'level'  : :level,  // a level object, containing a map and time data
    'cues'   : :cues,   // look :cues in GET /gofish/api/v2/game/
    'caught' : [],      // always empty
    'money'  : int,     // money the player has. Legacy from the times when starting a level had a cost
  }
  ```

* `GET /gofish/api/end/` -- End the current game

  A call to finish the current level. Must always be called, the game is never fishined automatically.
  
  Failure response:
  
  ```javascript
  {
    'error': string // an unhelpful error message, not really displayable
  }
  ```
  
  Success response:
  
  ```javascript
  {
    'earned'  : int, // how much money was earned in this game
    'maximum' : int, // what was the maximum to be earned in this game
    'avg'     : int, // what was the predicted average to earn in this game
    'money'   : int, // the current amount of money a player has
    'stars'   : int  // star-rating of performance. Bug: is 0 unless the player beats their highscore
  }
  ```

* `GET /gofish/api/action/move/:direction/` -- Move on a map in the given direction

  Moves on a map in a given direction.
  
  Request parameters:
  
  ```javascript
  :direction -> enum{'left', 'right'} // direction in which to move
  ```
  
  Failure response:
  
  ```javascript
  {
    'error': string // an unhelpful error message, not really displayable
  }
  ```
  
  Success response:
  
  ```javascript
  {
    'position' : int,   // the new position on the map
    'cues'     : :cues, // see :cues in GET /gofish/api/v2/game/
    'time'     : int,   // the time spent in the game so far
  }
  ```

* `GET /gofish/api/action/inspect/:N/` -- List of potential catches

  Get a list of stuff you'd catch if you fished in the current location `:N` times. 
  Useful for developing own cues instead of relying on the cues the game provides,
  as well as for novelty game mechanics in conjunction with `GET /gofish/api/action/catchnonil/`.
  
  Request paramters:
  
  ```javascript
  :N -> int, // the depth of inspection, e.g. 5 means look up what would happen in case the player
             // chose to fish for 5 consecutive times
  ```
  
  Failure response:
  
  ```javascript
  {
    'error': string // an unhelpful error message, not really displayable
  }
  ```
  
  Success response:
  
  ```javascript
  {
    'fishList': [:fish || null] // see :fish in GET /gofish/api/v2/game/
                                // null is used to indicate that nothing would be caught
                                // fishList.length <= :N
  }
  ```

* `GET /gofish/api/action/catchnonil/:listOfSuccess/` -- Catch specified fish, Nil yields skipped

  With this API call it is possible to specify exactly which fish to catch, skipping the Nil yields. 
  The potential use-case scenario would be if the game client allowed player to wait till the next fish is caught.
  The Nil yields would be treated as idle time, and thus it would be ignored when asking to catch a given fish.
  
  Request parameters:
  
  ```javascript
  :listOfSuccess -> string, // comma-separated string of 1's and 0's, indicating that the given fish
                            // was caught. For example: '1,0,1' means catch the first fish, skip the second,
                            // catch the third
                            // see test_game.py for a clearer example
  ```

  Failure response:
  
  ```javascript
  {
    'error': string // an unhelpful error message, not really displayable
  }
  ```
  
  Success response:
  
  ```javascript
  {
    'fishList' : [:fish], // the list of fish caught with this request,
                          // see :fish in GET /gofish/api/v2/game/
    'cues'     : :cues,   // see :cues in GET /gofish/api/v2/game/
    'time'     : int,     // the time spent in the game so far
  }
  ```
  
* `GET /gofish/api/action/catchall/:listOfSuccess/` -- Catch specified fish or nothing, without any skipping

  This API call is useful for discrete time fishing. IT is used to specify whether to catch or not whatever 
  is in the next yield.
  
  Request parameters:
  
  ```javascript
  :listOfSuccess -> string, // comma-separated string of 1's and 0's, indicating that the given yields
                            // to be extracted. For example: '1,0,1' means catch the first fish (or nothing)
                            // skip the second yield, catch the third fish (or nothing)
                            // see test_game.py for a clearer example
  ```

  Failure response:
  
  ```javascript
  {
    'error': string // an unhelpful error message, not really displayable
  }
  ```
  
  Success response:
  
  ```javascript
  {
    'fishList' : [:fish || null], // the list of fish caught with this request,
                                  // see :fish in GET /gofish/api/v2/game/
    'cues'     : :cues,           // see :cues in GET /gofish/api/v2/game/
    'time'     : int,             // the time spent in the game so far
  }
  ```

* `GET /gofish/api/update/:target/` -- Upgrade given category (boat, cues, etc.)

  Upgrade the boat, cues, or the fishing line to the next level, if one exists.
  
  Request parameters:
  
  ```javascript
  :target -> enum{'boats', 'cues', 'lines'} // the category to update
  ```

  Failure response:
  
  ```javascript
  {
    'error': string // an unhelpful error message, not really displayable
  }
  ```

  Success response is deprecated and should be treated as `200 OK`. The actual contents are:
  
  ```javascript
  {
    'player' : :player // serialised player object
  }
  ```
  
* `GET /gofish/api/buy/:bait/` -- Buy given bait

  Buy the specified bait, enabling choosing this bait afterwards.
  
  Request parameters:
  
  ```javascript
  :bait -> string // bait identification string, such as 'vobbler' or 'spinner'
  ```

  Failure response:
  
  ```javascript
  {
    'error': string // an unhelpful error message, not really displayable
  }
  ```

  Success response is deprecated and should be treated as `200 OK`. The actual contents are:
  
  ```javascript
  {
    'player' : :player // serialised player object
  }
  ```

* `GET /gofish/api/choose/:bait/` -- Choose to use given bait in fishing

  Choose to use the given bait for fishing. **Bug:** it is impossible to go back to not using any baits again.
  
  Request parameters:
  
  ```javascript
  :bait -> string // bait identification string, such as 'vobbler' or 'spinner'
  ```

  Failure response:
  
  ```javascript
  {
    'error': string // an unhelpful error message, not really displayable
  }
  ```

  Success response is deprecated and should be treated as `200 OK`. The actual contents are:
  
  ```javascript
  {
    'player' : :player // serialised player object
  }
  ```

* `GET /gofish/api/getmodifiers/` -- The baits that exist in the game

  Returns the complete reference of baits that exist in the game.
  
  Success response:
  
  ```javascript
  {':bait': {      //  :bait -> bait identification string, such as 'vobbler' or 'spinner'
    'fish_1': float, // multiplier of the probability to catch fish_1
    'fish_2': float  // multiplier of the probability to catch fish_2
  }}
  ```

* *Deprecated.* `GET /gofish/api/getgame/` -- Returns all relevant game info at once

* *Deprecated.* `GET /gofish/api/getupdates/` -- List of upgrades you can buy

## Modifying the code

## Optimising the game

## Analysing data

