from django.db import models
from copy import copy

# a data point for charting
class DataPoint(models.Model):
    # players username
    username  = models.TextField()
    # game number for this player
    gameNum   = models.IntegerField()
    # detauls for the cues
    cueDetail = models.IntegerField()
    # game level index
    level     = models.IntegerField()
    # move cost for the player
    moveCost  = models.IntegerField()
    # fishing cost for the player
    fishCost  = models.IntegerField()
    # is this an endgame location
    endGame   = models.IntegerField()
    # how much time did the player spend
    timeSpent = models.IntegerField()
    # how much time was it optimal to spend
    optTime   = models.IntegerField()
    # local optimum for the time
    locOptT   = models.IntegerField()
    # how much money did the player earned
    earnedM   = models.IntegerField()
    # how much money would optimum bring
    optimalM  = models.IntegerField()
    # how much money would local optimum bring
    locOptM   = models.IntegerField()
    # time the datapoint was recorded
    createdAt = models.IntegerField()

    def __unicode__(self):
        'a data point'

    def toDict(self):
        d = copy(self.__dict__)
        d['_state'] = None
        return d

    #############################################################
    # creators
    #############################################################
    # take a line from log and store it in the database
    @staticmethod
    def insertFromLine(line):
        # our data is space separated
        line = line.split(' ')

        # create a data point
        point = DataPoint(
            username  = line[0],
            gameNum   = int(line[1]),
            cueDetail = int(line[2]),
            level     = int(line[3]),
            moveCost  = int(line[4]),
            fishCost  = int(line[5]),
            endGame   = int(line[6]),
            timeSpent = int(line[7]),
            optTime   = int(line[8]),
            locOptT   = int(line[9]),
            earnedM   = int(line[10]),
            optimalM  = int(line[11]),
            locOptM   = int(line[12]),
            createdAt = int(line[13]))

        # store it
        point.save()

    #############################################################
    # accessors
    #############################################################
    # return all data points for a query
    @staticmethod
    def query(username=None, gameNum=None, cueDetail=None,
              level=None, moveCost=None, endGame=None):
        qs = DataPoint.objects.all()

        if None != username:  qs = qs.filter(username=username)
        if None != gameNum:   qs = qs.filter(gameNum=gameNum)
        if None != cueDetail: qs = qs.filter(cueDetail=cueDetail)
        if None != level:     qs = qs.filter(level=level)
        if None != moveCost:  qs = qs.filter(moveCost=moveCost)
        if None != endGame:   qs = qs.filter(endGame=endGame)

        qs = qs.order_by('id')

        return qs

    # return overall info about our data
    @staticmethod
    def describeData():
        qs = DataPoint.objects.all();
        return {
            'usernames'  : qs.values('username').distinct(),
            'gameNums'   : qs.values('gameNum').distinct(),
            'cueDetails' : qs.values('cueDetail').distinct(),
            'levels'     : qs.values('level').distinct(),
            'moveCosts'  : qs.values('moveCost').distinct()
        }

    #############################################################
    # Django boilerplate
    #############################################################
    # this has to be included to make Django realise
    # that this model belongs to the app
    class Meta:
        app_label = 'charts'

