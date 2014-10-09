from django.db import models
from django.contrib.auth.models import User
import json
import gamedef

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
        for key in self.updates:
            if 'time' in self.updates[key]:
                cost += self.updates[key]['time']
        return cost

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
        if self.player.money < 10:
            self.player.money = 10
        self.player.savePlayer()

        self.delete()
        return earned

    # a method to move player on the map
    def move(self, direction):
        size = len(self.level['map'][0])
        position = self.level['position']
        self.player.unmarshal()
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
            'time': time
        }

    # a method to marshal fields
    def marshal(self):
        if not isinstance(self.level, basestring):
            self.level = json.dumps(self.level)
        if not isinstance(self.caught, basestring):
            self.caught = json.dumps(self.caught)

    # a method to unmarshal fields
    def unmarshal(self):
        if isinstance(self.level, basestring):
            self.level = json.loads(self.level)
        if isinstance(self.caught, basestring):
            self.caught = json.loads(self.caught)

    # a special save method, to ensure, that we
    # serialise our fields
    def saveGame(self):
        self.marshal()
        self.save()
        self.unmarshal()
    
    def __unicode__(self):
        return self.player.user.username + ' game'
