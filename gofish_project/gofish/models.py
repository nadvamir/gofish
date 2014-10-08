from django.db import models
from django.contrib.auth.models import User

# a player of the game
class Player(models.Model):
    user      = models.OneToOneField(User)

    # how much currency this player has
    money     = models.IntegerField(default=10)
    # what updates has it bought (JSON)
    updates   = models.TextField()
    # what modifiers does it has (JSON)
    modifiers = models.TextField()

    def __unicode__(self):
        return self.user.username + ' player'

# a game class, representing the current level and everything
# that happens in it
class Game(models.Model):
    player = models.OneToOneField(Player)
    # a json representation of the current level
    level  = models.TextField()
    # a json representation of the fish caught
    caught = models.TextField()
    
    def __unicode__(self):
        return self.player.user.username + ' game'
