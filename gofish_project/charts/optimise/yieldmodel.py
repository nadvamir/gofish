from constraint import *
import gofish.engine.gamedef as gamedef
from yieldcalculator import YieldCalculator

class YieldModel(object):
    def __init__(self, yields):
        # create a constraint problem
        self.problem = Problem()
        # save reference to yields
        self.yields = yields

        # add variables for fish prices
        #self.problem.addVariable('shoe', range(1, 10))
        #self.problem.addVariable('bass', range(3, 20))
        #self.problem.addVariable('brime', range(7, 30))
        #self.problem.addVariable('pike', range(17, 50))
        #self.problem.addVariable('catfish', range(41, 100))
        self.problem.addVariable('shoe', [1])
        self.problem.addVariable('bass', [3])
        self.problem.addVariable('brime', [7])
        self.problem.addVariable('pike', [17])
        self.problem.addVariable('catfish', [200])

        # add variables for level costs
        # (first one is free):
        self.problem.addVariable(1, range(50, 200))
        self.problem.addVariable(2, range(200, 1000))
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

    # this thing actually tries to optimise the result
    # because the domain space is too big to solve...
    # should probably rename it...
    def optimise(self):
        print 'solving...'
        it = self.problem.getSolutionIter()
        solution = {}
        minCost = 1 << 20
        n0 = gamedef.GAME['levels'][0]['timesToPlay']
        n1 = gamedef.GAME['levels'][1]['timesToPlay']

        try:
            for i in range(1000000):
                s = it.next()
                optY0 = YieldCalculator.getOptYield(s, self.yields[0])
                optY1 = YieldCalculator.getOptYield(s, self.yields[1])
                cost0 = abs(optY0 * n0 - s[1])
                cost1 = abs(optY1 * n1 - s[2])
                cost = cost0 + cost1
                if cost < minCost:
                    minCost = cost
                    solution = s
                if i % 10000 == 0:
                    print i, ': ', s, cost
        except StopIteration:
            print 'reached end'

        print 'solution:', solution
        print 'min cost:', minCost
        return {
            'solution' : solution,
            'minCost' : minCost,
        }

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
            optYield = YieldCalculator.getOptYield(fish, self.yields[level])

            # the actual constraint:
            return optYield * gamedef.GAME['levels'][level]['timesToPlay'] >= cost


        self.problem.addConstraint(
                progressionConstraint,
                (level+1, 'shoe', 'bass', 'brime', 'pike', 'catfish'))

