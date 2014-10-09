import maps
import yields

# here we have a GAME definition object, already priced
TOTAL_TIME = 480
GAME = {
    'fish': {
        'shoe': {
            'name': 'Shoe',
            'value': 1,
            'weight': 0.3,
            'length': 30,
        },
        'bass': {
            'name': 'Bass',
            'value': 3,
            'weight': 0.2,
            'length': 15,
        },
        'brime': {
            'name': 'Brime',
            'value': 7,
            'weight': 1.0,
            'length': 40,
        },
        'pike': {
            'name': 'Pike',
            'value': 17,
            'weight': 1.5,
            'length': 50,
        },
        'catfish': {
            'name': 'Catfish',
            'value': 41,
            'weight': 10.0,
            'length': 100,
        },
    },

    'levels': [{
        'name': 'Local pond',
        'fish': {
            'shoe': 0.7,
            'bass': 0.3,
        },
        'cost': 10,
        'distribution': 'uniform-declining',
      }, {
        'name': 'Lake',
        'fish': {
            'bass': 0.6,
            'brime': 0.4,
            'pike': 0.3,
        },
        'cost': 100,
        'distribution': 'natural-declining',
      }, {
        'name': 'River',
        'fish': {
            'bass': 0.7,
            'pike': 0.3,
            'catfish': 0.1,
        },
        'cost': 1000,
        'distribution': 'natural-declining-endspike',
    }],
}

# a function to get the fish for this level
def getFishForLevel(level):
    fishList = []
    for fish, prob in GAME['levels'][level]['fish'].iteritems():
        newFish = (GAME['fish'][fish])
        newFish['probability'] = prob
        fishList.append(newFish)
    return fishList

# a function to get the level dict
def getLevel(level):
    lvl = dict(GAME['levels'][level])
    lvl['index'] = level
    lvl['time'] = 0
    lvl['map'] = maps.generate(maxDepth=10, width=20)
    lvl['position'] = 0

    # time spent in each location
    lvl['timeInLoc'] = [0 for i in range(20)]

    # yields are not yet defined
    lvl['yields'] = [None for i in range(20)]

    return lvl

# compute a new yield function for the specified location
def setYieldFor(game, pos):
    target = 40
    if level == 1:
        target = 300
    elif level > 1:
        target = 1300

    game.level['yields'][pos] = yields.getTargetYield(TOTAL_TIME, target, getFishForLevel(game.level.index))
