from constraint import *
import gofish.engine.gamedef as gamedef

class YieldModel(object):
    def __init__(self, yields):
        # create a constraint problem
        self.problem = Problem()
        # save reference to yields
        self.yields = yields

        # add variables for fish prices
        self.problem.addVariable('shoe', range(1, 10))
        self.problem.addVariable('bass', range(3, 20))
        self.problem.addVariable('brime', range(7, 30))
        self.problem.addVariable('pike', range(17, 50))
        self.problem.addVariable('catfish', range(41, 100))

        # add variables for level costs
        # (first one is free):
        self.problem.addVariable(1, range(50, 200))
        self.problem.addVariable(2, range(200, 2000))
        numLvl = len(gamedef.GAME['levels'])

        # now, setting up the constraints
        less = lambda a, b: a < b

        # every cooler fish is more expensive
        self.problem.addConstraint(less, ('shoe', 'bass'))
        self.problem.addConstraint(less, ('bass', 'brime'))
        self.problem.addConstraint(less, ('brime', 'pike'))
        self.problem.addConstraint(less, ('pike', 'catfish'))

        # for every level up to last:
        for i in range(numLvl - 1):
            self._constrainLevel(i)

    def solve(self):
        print 'solving...'
        it = self.problem.getSolutionIter()
        solution = {}; minCost = 1 << 20
        try:
            for i in range(100000):
                s = it.next()
                cost = abs(self._getOptYield(s, 0) - s[1]) + abs(self._getOptYield(s, 1) - s[2])
                if cost < minCost:
                    minCost = cost
                    solution = s
                if i % 10000 == 0:
                    print i, ': ', s, cost
        except StopIteration:
            print 'reached end'
        print solution
        print minCost
        print self._getOptYield(solution, 0)
        return {}

        solutions = self.problem.getSolutions()
        print 'found ' + len(solutions) + ' solutions.'
        if len(solutions) > 0:
            print solutions[0]
        return {}

    # constraining a level
    def _constrainLevel(self, level):
        # the optimal yield * timesToPlay ~= cost of level + 1
        def progressionConstraint(cost, shoe, bass, brime, pike, catfish):
            # enclosing calculated fish prices back to dict
            fish = {
                'shoe': shoe,
                'bass': bass,
                'brime': brime,
                'pike': pike,
                'catfish': catfish
            }

            # getting the optimal yield for this level
            optYield = self._getOptYield(fish, level)

            # the actual constraint:
            return optYield * gamedef.GAME['levels'][level]['timesToPlay'] >= cost


        self.problem.addConstraint(
                progressionConstraint,
                (level+1, 'shoe', 'bass', 'brime', 'pike', 'catfish'))

    # calculating optimal yield for the level
    def _getOptYield(self, fish, level):
        # for now, static parameters:
        time = 480.0
        fishingCost = 5.0
        movingCost = 30.0

        # optimal yield is that, which maximises
        # the overall yield of the game
        maxYield = 0.0
        for i in range(len(self.yields[level])):
            y = 0.0
            # yield from one location
            for f, n in self.yields[level][i].iteritems():
                y += fish[f] * n
            # yield overall from a game
            y *= time / ((i + 1) * fishingCost + movingCost)
            # saving the largest so far:
            if maxYield < y:
                maxYield = y

        return maxYield
