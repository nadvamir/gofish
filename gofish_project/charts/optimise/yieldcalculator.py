import gofish.engine.gamedef as gamedef
import gofish.models as models

# a simulator, that calculates average yields
# for every game level
class YieldCalculator(object):
    ############################################################
    # Public API
    ############################################################
    # return yields for every level
    # that are expressed as fish per fishing time in loc
    @staticmethod
    def getYields():
        yields = []
        player = models.Player.stub()

        for i in range(len(gamedef.GAME['levels'])):
            yc = YieldCalculator(player, gamedef.getLevel(i))
            yields.append(yc.simulate())

        return yields

    ############################################################
    # MonteCarlo internals
    ############################################################
    # create an instance of calculator for one level
    def __init__(self, player, level):
        self.player = player
        self.level  = level

    # run a simulation
    def simulate(self):
        nTimes, y = self.getInitY()

        N = 100
        for n in range(N):
            instance = self.getYield()
            for i in range(len(instance)):
                for fish, amount in instance[i].iteritems():
                    y[i][fish] += amount / N

        return y

    # get an average yield of a level
    def getYield(self):
        # create a game stub
        game = models.Game.stub(self.player, self.level)

        # set yields for every position
        nPos = len(game.level['yields'])
        for i in range(nPos):
            game.setYieldFor(i)

        # aggregate the yield
        nTimes, y = self.getInitY()
        for i in range(nPos):
            for j in range(nTimes):
                if None != game.level['yields'][i][j]:
                    y[j][game.level['yields'][i][j]['id']] += \
                            1.0 / nPos
        return y

    # get initial yield for the level
    def getInitY(self):
        nTimes = gamedef.TOTAL_TIME / 5 # 5 is fishing time
        y = [toYield(gamedef.getFishForLevel(self.level['index'])) \
                for i in range(nTimes)]
        return nTimes, y

# a function to convert a list of fish to yield
def toYield(l):
    y = {}
    for fish, whatever in l.iteritems():
        y[fish] = 0.0
    return y
