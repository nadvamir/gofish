# a simulator, that calculates average yields
# for every game level
class YieldCalculator(object):
    ############################################################
    # Public API
    ############################################################
    # return yields for every level
    @staticmethod
    def getYields():
        return []

    ############################################################
    # MonteCarlo internals
    ############################################################
    # create an instance of calculator for one level
    def __init__(self, player, level):
        pass

    # run a simulation
    def simulate(self):
        pass

    # get an average yield of a level
    def getYield(self):
        pass

