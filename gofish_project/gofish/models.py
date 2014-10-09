from django.db import models
from django.contrib.auth.models import User
import json

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
        self.player.savePlayer()

        self.delete()
        return earned

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
