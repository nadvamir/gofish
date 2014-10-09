# here we have a game definition object, already priced
game = {
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
        'cost': 100,
        'distribution': 'natural-declining-endspike',
    }],
}

# a function to get the fish for this level
def getFishForLevel(level):
    fishList = []
    for fish, prob in game['levels'][level]['fish'].iteritems():
        newFish = (game['fish'][fish])
        newFish['probability'] = prob
        fishList.append(newFish)
    return fishList

