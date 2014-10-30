from django.db import models
from django.contrib.auth.models import User
import json
import gamedef
import cues

MIN_MONEY = 10

# a player of the game
class Player(models.Model):
    user      = models.OneToOneField(User)

    # how much currency this player has
    money     = models.IntegerField(default=10)
    # what updates has it bought (JSON)
    updates   = models.TextField(default='{}')
    # what modifiers does it has (JSON)
    modifiers = models.TextField(default='{}')

    # a method to get initialised player object
    @staticmethod
    def initialise(user):
        player = None

        # try to find existing player
        try:
            player = Player.objects.get(user=user)
        # if there is none, create a new one
        except Player.DoesNotExist:
            player = Player(user=user)
            player.save()

        # unmarshal json fields
        player.unmarshal()

        return player

    # returns movement cost of this player
    def getMoveCost(self):
        cost = 30
        upds = gamedef.GAME['updates']
        for key in self.updates:
            for v in upds[key]:
                if self.updates[key] == v['name'] and 'time' in v:
                    cost += v['time']
        return cost

    # returns the level of detail of cues
    def getCueDetail(self):
        if 'cues' not in self.updates:
            return 0

        upds = gamedef.GAME['updates']
        for v in upds['cues']:
            if self.updates['cues'] == v['name']:
                return v['cueDetail']

    # return a bait that the player has selected
    def getSelectedBait(self):
        for bait in self.modifiers.iterkeys():
            if self.modifiers[bait]:
                return gamedef.GAME['modifiers'][bait]
        return None

    # returns if there is enough money to buy something
    # a minimum has to remain, otherwise fishing is impossible
    def hasEnoughFor(self, amount):
        return self.money - MIN_MONEY >= amount

    # augment probability to catch a fiven fish
    def augmentProb(self, fish, probability):
        # fist of all, special items
        upds = gamedef.GAME['updates']
        for key in self.updates:
            for v in upds[key]:
                if self.updates[key] == v['name'] and 'probability' in v:
                    probability += v['probability'] - 1

        # then check if the bait has any effect
        bait = self.getSelectedBait()
        if bait and fish in bait:
            probability *= bait[fish]

        return probability

    # tries to update a given target
    def update(self, target):
        if target in gamedef.GAME['updates']:
            # find the next update
            upds = gamedef.GAME['updates'][target]
            update = upds[0]
            if target in self.updates:
                for i in range(len(upds)):
                    if upds[i]['name'] == self.updates[target]:
                        if i < len(upds) - 1:
                            update = upds[i+1]
                            break
                        else:
                            return False
            # buy it
            if self.hasEnoughFor(update['price']):
                self.money -= update['price']
                self.updates[target] = update['name']
                self.savePlayer()
                return True
        return False

    # tries to select a given bait
    def choose(self, bait):
        # bait doesn't exist
        if bait not in self.modifiers:
            return False

        # unselect all baits
        for k in self.modifiers.iterkeys():
            self.modifiers[k] = False

        # select bait
        self.modifiers[bait] = True
        self.savePlayer()

        # recalculate yields if there are any
        game = Game.initialise(self)
        if None != game:
            game.recalcYields()
        return True

    # tries to buy a given bait
    def buy(self, bait):
        # bait doesn't exist
        if bait not in gamedef.GAME['modifiers']:
            return False
        # bait is already bought
        if bait in self.modifiers:
            return False

        baitObj = gamedef.GAME['modifiers'][bait]
        # not enough money
        if not self.hasEnoughFor(baitObj['price']):
            return False

        self.money -= baitObj['price']
        self.modifiers[bait] = False # not selected by default
        self.savePlayer()
        return True

    # a method to marshal fields
    def marshal(self):
        if not isinstance(self.updates, basestring):
            self.updates = json.dumps(self.updates)
        if not isinstance(self.modifiers, basestring):
            self.modifiers = json.dumps(self.modifiers)

    # a method to unmarshal fields
    def unmarshal(self):
        if isinstance(self.updates, basestring):
            self.updates = json.loads(self.updates)
        if isinstance(self.modifiers, basestring):
            self.modifiers = json.loads(self.modifiers)

    # a special save method, to ensure, that we
    # serialise our fields
    def savePlayer(self):
        self.marshal()
        self.save()
        self.unmarshal()

    def toDict(self):
        return {
            'money': self.money,
            'updates': self.updates,
            'modifiers': self.modifiers,
        }

    def __unicode__(self):
        return self.user.username + ' player'

# a game class, representing the current level and everything
# that happens in it
class Game(models.Model):
    player = models.OneToOneField(Player)
    # a json representation of the current level
    level  = models.TextField(default='{}')
    # a json representation of the fish caught
    caught = models.TextField(default='[]')
    
    # a method to get initialised game object
    @staticmethod
    def initialise(player, level=None):
        game = None

        # try to find existing game
        try:
            game = Game.objects.get(player=player)
        # if there is none, create a new one
        except Game.DoesNotExist:
            # if we did not specify level, this means
            # that we don't want to create a game
            if None == level:
                return None
            # if there is not enough money, return None
            if player.money < level['cost']:
                return None
            # remove the price of the level from player
            player.money -= level['cost']
            player.savePlayer()

            game = Game(player=player, level=json.dumps(level))
            game.save()

        # unmarshal json fields
        game.unmarshal()
        if level and game.level['index'] != level['index']:
            # or, maybe end the previous game and start a new one
            return None

        return game

    # a special delete method, that calculates the value
    # of the fish caught, and rewards the player
    def deleteGame(self):
        earned = 0
        for fish in self.caught:
            earned += fish['value']
        self.player.money += earned
        if self.player.money < MIN_MONEY:
            self.player.money = MIN_MONEY
        self.player.savePlayer()

        self.delete()
        return earned

    # returns cues for the current fishing position
    def getCues(self):
        pos = self.level['position']
        # create yields if they are not present
        if None == self.level['yields'][pos]:
            gamedef.setYieldFor(self, pos)
            self.saveGame()

        # now delegate to the cue class
        return cues.generate(self, pos)

    # a method to move player on the map
    def move(self, direction):
        size = len(self.level['map'][0])
        position = self.level['position']
        cost = self.player.getMoveCost()

        step = -1
        if direction == 'right':
            step = 1

        position += step
        if position < 0 or position >= size:
            return None

        if self.level['time'] + cost > self.level['totalTime']:
            return None

        self.level['position'] = position
        self.level['time'] += cost
        self.saveGame()
        return {
            'position': position,
            'cues': self.getCues(),
            'time': self.level['time'],
        }

    # a method to fish
    # it only really returns what you can catch in N steps
    # from the current point, you need to call catch action
    # to actually advance timer
    def fish(self, steps):
        pos = self.level['position']
        if None == self.level['yields'][pos]:
            gamedef.setYieldFor(self, pos)
            self.saveGame()

        spotYield = self.level['yields'][pos]
        spotTime = self.level['timeInLoc'][pos]
        maxSteps = len(spotYield) - spotTime
        if steps > maxSteps:
            steps = maxSteps
        print steps

        stepCost = self.level['totalTime'] / len(spotYield)
        expectedEndTime = steps * stepCost + self.level['time'] 
        if expectedEndTime > self.level['totalTime']:
            return None

        return {
            'fishList': spotYield[spotTime:spotTime + steps]
        }

    # a method to actually catch the next N fish
    def catch(self, fishList):
        pos = self.level['position']
        if None == self.level['yields'][pos]:
            return None

        spotYield = self.level['yields'][pos]
        spotTime = self.level['timeInLoc'][pos]
        time = self.level['time']
        totalTime = self.level['totalTime']
        stepCost = totalTime / len(spotYield)

        caught = []
        for succeeded in fishList:
            while (spotTime < len(spotYield)
                and spotYield[spotTime] == None):
                    time += stepCost
                    spotTime += 1

            if time > totalTime or spotTime == len(spotYield):
                break

            if '1' == succeeded:
                caught.append(spotYield[spotTime])

            time += stepCost
            spotTime += 1

        self.caught += caught
        self.level['time'] = time
        self.level['timeInLoc'][pos] = spotTime
        self.saveGame()

        return {
            'fishList': caught,
            'cues': self.getCues(),
            'time': time
        }

    # a method to actually catch the next N fish or nothings
    def catchAll(self, fishList):
        pos = self.level['position']
        if None == self.level['yields'][pos]:
            gamedef.setYieldFor(self, pos)
            self.saveGame()

        spotYield = self.level['yields'][pos]
        spotTime = self.level['timeInLoc'][pos]
        time = self.level['time']
        totalTime = self.level['totalTime']
        stepCost = totalTime / len(spotYield)

        caught = []
        response = []
        for succeeded in fishList:
            if time > totalTime or spotTime == len(spotYield):
                break

            if '1' == succeeded and None != spotYield[spotTime]:
                caught.append(spotYield[spotTime])
                response.append(spotYield[spotTime])
            else:
                response.append(None)

            time += stepCost
            spotTime += 1

        self.caught += caught
        self.level['time'] = time
        self.level['timeInLoc'][pos] = spotTime
        self.saveGame()

        return {
            'fishList': response,
            'cues': self.getCues(),
            'time': time
        }

    # recalculate all the yields for this game
    def recalcYields(self):
        for pos in range(len(self.level['yields'])):
            if self.level['yields'][pos]:
                gamedef.setYieldFor(self, pos)

    # a method to marshal fields
    def marshal(self):
        if not isinstance(self.level, basestring):
            self.level = json.dumps(self.level)
        if not isinstance(self.caught, basestring):
            self.caught = json.dumps(self.caught)
        # no need to marshal the player here

    # a method to unmarshal fields
    def unmarshal(self):
        if isinstance(self.level, basestring):
            self.level = json.loads(self.level)
        if isinstance(self.caught, basestring):
            self.caught = json.loads(self.caught)
        # unmarshal player as well, to make life easy
        self.player.unmarshal()

    # a special save method, to ensure, that we
    # serialise our fields
    def saveGame(self):
        self.marshal()
        self.save()
        self.unmarshal()
    
    def __unicode__(self):
        return self.player.user.username + ' game'
