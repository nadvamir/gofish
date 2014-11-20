from django.db import models

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

    def __unicode__(self):
        'a data point'

    #############################################################
    # Django boilerplate
    #############################################################
    # this has to be included to make Django realise
    # that this model belongs to the app
    class Meta:
        app_label = 'charts'

