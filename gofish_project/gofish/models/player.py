from django.db import models
from django.contrib.auth.models import User
import json
import gofish.engine.gamedef as gamedef

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

    ##############################################################
    # access
    ##############################################################
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

    def toDict(self):
        return {
            'money': self.money,
            'updates': self.updates,
            'modifiers': self.modifiers,
        }

    def __unicode__(self):
        return self.user.username + ' player'

    ##############################################################
    # helpers
    ##############################################################
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

    ##############################################################
    # actions
    ##############################################################
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

    ##############################################################
    # Django boilerplate
    ##############################################################
    # this has to be included to make Django realise
    # that this model belongs to the app
    class Meta:
        app_label = 'gofish'

