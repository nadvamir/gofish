from constraint import *
import gofish.engine.gamedef as gamedef
from yieldcalculator import YieldCalculator
from yieldcalculator import MOV_C

class YieldModel(object):
    def __init__(self, yields):
        # create a constraint problem
        self.problem = Problem()
        # save reference to yields
        self.yields = yields

        # add variables for fish prices
        #self.problem.addVariable('shoe', range(1, 10))
        self.problem.addVariable('shoe', range(1, 2))
        #self.problem.addVariable('bass', range(3, 20))
        self.problem.addVariable('bass', range(3, 4))
        #self.problem.addVariable('brime', range(7, 30))
        self.problem.addVariable('brime', range(26, 27))
        #self.problem.addVariable('pike', range(17, 50))
        self.problem.addVariable('pike', range(29, 30))
        #self.problem.addVariable('cod', range(120, 200))
        self.problem.addVariable('cod', range(144, 145))
        self.problem.addVariable('carp', range(180, 181))
        self.problem.addVariable('catfish', range(200, 201))
        self.problem.addVariable('tuna', range(1000, 1001))

        # add variables for level costs
        # (first one is free):
        #self.problem.addVariable(1, range(120, 121))
        numLvl = 5

        # now, setting up the constraints
        less = lambda a, b: a < b

        # every cooler fish is more expensive
        self.problem.addConstraint(less, ('shoe', 'bass'))
        self.problem.addConstraint(less, ('bass', 'brime'))
        self.problem.addConstraint(less, ('brime', 'pike'))
        self.problem.addConstraint(less, ('pike', 'cod'))
        self.problem.addConstraint(less, ('cod', 'carp'))
        self.problem.addConstraint(less, ('carp', 'catfish'))
        self.problem.addConstraint(less, ('catfish', 'tuna'))

        # for every level up to last:
        for i in range(numLvl - 1):
            self._constrainLevel(i)

    # this thing actually tries to optimise the result
    # because the domain space is too big to solve...
    # should probably rename it...
    def optimise(self):
        print 'getting iterator...'
        it = self.problem.getSolutionIter()
        print 'we have one'
        solution = {}
        maxDiff = 0
        levels = gamedef.GAME['levels']
        nLvl = len(levels)

        try:
            for i in range(1000000):
                s = it.next()
                diff = 0.0
                optY = YieldCalculator.getOptYield(s, self.yields[0], MOV_C[0])
                for l in range(1, nLvl):
                    nOptY = YieldCalculator.getOptYield(s, self.yields[l], MOV_C[l])
                    diff += abs(nOptY/float(optY))
                    optY = nOptY

                if diff > maxDiff:
                    maxDiff = diff
                    solution = s
                if i % 10000 == 0:
                    print i, ': ', s, diff
        except StopIteration:
            print 'reached end'

        print 'solution:', solution
        print 'max diff:', maxDiff
        return {
            'solution' : solution,
            'maxDiff' : maxDiff,
        }

    # constraining a level
    def _constrainLevel(self, level):
        a = [0]
        # the optimal yield * timesToPlay ~= cost of level + 1
        def progressionConstraint(shoe, bass, brime, pike, catfish, cod, tuna, carp):
            global i
            # enclosing calculated fish prices back to dict
            fish = {
                'shoe': shoe,
                'bass': bass,
                'brime': brime,
                'pike': pike,
                'catfish': catfish,
                'cod': cod,
                'tuna': tuna,
                'carp': carp
            }

            # getting the optimal yield for this level
            optYield1 = YieldCalculator.getOptYield(fish,
                    self.yields[level], MOV_C[level])
            # getting the optimal yield for next level
            optYield2 = YieldCalculator.getOptYield(fish,
                    self.yields[level+1], MOV_C[level+1])

            if a[0] % 100000 == 0:
                print a[0], shoe, bass, brime, pike, catfish, cod, tuna, carp, '-', optYield1, optYield2
            a[0] += 1

            # the actual constraint:
            return optYield2 > optYield1

        self.problem.addConstraint(
                progressionConstraint,
                ('shoe', 'bass', 'brime', 'pike', 'catfish', 'cod', 'tuna', 'carp'))

