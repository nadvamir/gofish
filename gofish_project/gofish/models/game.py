from django.db import models
from django.contrib.auth.models import User
import json
import logging
import time

from player import Player
from gofish.engine.yieldmerger import YieldMerger
from gofish.engine.cues import *
import gofish.engine.gamedef as gamedef

MIN_MONEY = 10

generators = [
    lambda g, p: BaseCue().get(),                     # no cues
    lambda g, p: DepthCue(g, p).get(),                # map
    lambda g, p: UniformNoiseCue(g, p, 4, 0.5).get(), # camera
    lambda g, p: UniformNoiseCue(g, p, 7, 0.7).get(), # old sonar
    lambda g, p: UniformNoiseCue(g, p, 10, 0.85).get(), # sonar
    lambda g, p: FishCue(g, p, 10).get()              # mermaid
]

# a game class, representing the current level and everything
# that happens in it
class Game(models.Model):
    player = models.OneToOneField(Player)
    # a json representation of the current level
    level  = models.TextField(default='{}')
    # a json representation of the fish caught
    caught = models.TextField(default='[]')
    
    ##############################################################
    # access
    ##############################################################
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
            # update the number of games for this player
            player.numGames += 1
            # save changes to player
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
        # log the players performance for the research
        # (counting end game in the same fashion, as move)
        self.logPerformance(True)

        earned = 0
        for fish in self.caught:
            earned += fish['value']
        self.player.money += earned
        if self.player.money < MIN_MONEY:
            self.player.money = MIN_MONEY
        self.player.savePlayer()

        self.delete()
        return earned

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
        return str(self.player) + ' ' + str(self.level['index'])

    ##############################################################
    # external helpers
    ##############################################################
    # returns cues for the current fishing position
    def getCues(self):
        pos = self.level['position']
        self.ensureYieldsExist(pos)
        # get the level of detail
        detail = self.player.getCueDetail()
        # create a specific cue for that level of detail
        return generators[detail](self, pos)
    
    # returns the depth of a spot on the map
    def getDephFor(self, position):
        return self.level['map'][0][position]

    # a function that returns the list of fishes in the yield
    def getFishInYield(self, pos):
        fish = {}
        # initial list
        yields = self.level['yields'][pos]
        for i in range(self.level['timeInLoc'][pos], len(yields)):
            if None != yields[i]:
                addFishToDict(fish, yields[i])

        # add prefered depth
        for k, v in fish.iteritems():
            v['depth'] = getPreferedDepth(k)

        return fish

    # create yields if they are not present
    def ensureYieldsExist(self, pos):
        if None == self.level['yields'][pos]:
            self.setYieldFor(pos)
            self.saveGame()

    # recalculate all the yields for this game
    def recalcYields(self):
        for pos in range(len(self.level['yields'])):
            if self.level['yields'][pos]:
                self.setYieldFor(pos)

    # compute a new yield function for the specified location
    def setYieldFor(self, pos):
        # setup some variables
        player = self.player
        fish = gamedef.getFishForLevel(self.level['index'])
        yieldMerger = YieldMerger(480/5)
        depth = self.level['map'][0][pos]

        # add yields for every fish
        for fishId, f in fish.iteritems():
            yieldMerger.addYield(fishId, f, depth, player)

        # get the combined yield
        self.level['yields'][pos] = yieldMerger.merge()

    # returns optimal time to spend in the given location
    def getOptimalTime(self, pos, local = False):
        self.ensureYieldsExist(pos)

        maxVal = 0.0
        bestTime = 0
        val = 0.0
        time = 1
        fishingCost = 5
        travelCost = self.player.getMoveCost() if pos > 0 else 0

        for fish in self.level['yields'][pos]:
            if None != fish:
                val += fish['value']
            if val / (time * fishingCost + travelCost) > maxVal:
                maxVal = val / (time * fishingCost + travelCost)
                bestTime = time
            elif val / (time*fishingCost + travelCost) < maxVal\
                    and True == local:
                # local optima found
                return bestTime
            time += 1

        return bestTime

    # returns how much money was earned in loc till given time
    def getMoneyEarnedIn(self, pos, timeSpent):
        earned = 0
        fish = self.level['yields'][pos]
        for i in range(0, timeSpent):
            if None != fish[i]:
                earned += fish[i]['value']
        return earned

    # a method to log users performance
    def logPerformance(self, endGame = False):
        logger = logging.getLogger('gofish')

        levelInfo   = str(self)
        pos         = self.level['position']
        timeSpent   = self.level['timeInLoc'][pos]
        optimalTime = self.getOptimalTime(pos)
        localOptT   = self.getOptimalTime(pos, local=True)
        moneyEarned = str(int(self.getMoneyEarnedIn(pos, timeSpent)))
        optimalM    = str(int(self.getMoneyEarnedIn(pos, optimalTime)))
        localOptM   = str(int(self.getMoneyEarnedIn(pos, localOptT)))
        endGame     = '1' if endGame else '0'
        moveCost    = str(self.player.getMoveCost())
        fishCost    = '5'
        createdAt   = str(int(round(time.time())))

        msg = [
            levelInfo, moveCost, fishCost, endGame,
            str(timeSpent), str(optimalTime), str(localOptT),
            moneyEarned, optimalM, localOptM,
            createdAt
        ]

        logger.info(' '.join(msg))

    #############################################################
    # actions
    #############################################################
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

        # log the players performance for the research
        self.logPerformance()

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
        self.ensureYieldsExist(pos)

        spotYield = self.level['yields'][pos]
        spotTime = self.level['timeInLoc'][pos]
        maxSteps = len(spotYield) - spotTime
        if steps > maxSteps:
            steps = maxSteps

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
        self.ensureYieldsExist(pos)

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

            if time + stepCost > totalTime or spotTime == len(spotYield):
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
        self.ensureYieldsExist(pos)

        spotYield = self.level['yields'][pos]
        spotTime = self.level['timeInLoc'][pos]
        time = self.level['time']
        totalTime = self.level['totalTime']
        stepCost = totalTime / len(spotYield)

        caught = []
        response = []
        for succeeded in fishList:
            if time + stepCost > totalTime or spotTime == len(spotYield):
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

    ##############################################################
    # Django boilerplate
    ##############################################################
    # this has to be included to make Django realise
    # that this model belongs to the app
    class Meta:
        app_label = 'gofish'

##############################################################
# internal helper functions
##############################################################
# adds fish to a given fish dict, for cues
def addFishToDict(fishDict, fish):
    if fish['name'] not in fishDict:
        fishDict[fish['name']] = {'weight': 0.0, 'count': 0}
    fishDict[fish['name']]['weight'] += fish['weight']
    fishDict[fish['name']]['count'] += 1

# a function that gets the preferred depth of a fish
def getPreferedDepth(fishName):
    for k, v in gamedef.GAME['fish'].iteritems():
        if fishName == v['name']:
            return v['habitat']
    return -1

