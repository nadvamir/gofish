import maps

# here we have a GAME definition object, already priced
TOTAL_TIME = 480
GAME = {
    'fish': {
        'shoe': {
            'id': 'shoe',
            'name': 'Shoe',
            'value': 1,
            'weight': 0.3,
            'length': 30,
            'habitat': 1,
        },
        'bass': {
            'id': 'bass',
            'name': 'Bass',
            'value': 3,
            'weight': 0.2,
            'length': 15,
            'habitat': 4,
        },
        'brime': {
            'id': 'brime',
            'name': 'Brime',
            'value': 7,
            'weight': 1.0,
            'length': 40,
            'habitat': 6,
        },
        'pike': {
            'id': 'pike',
            'name': 'Pike',
            'value': 17,
            'weight': 1.5,
            'length': 50,
            'habitat': 3,
        },
        'catfish': {
            'id': 'catfish',
            'name': 'Catfish',
            'value': 200,
            'weight': 10.0,
            'length': 100,
            'habitat': 9,
        },
    },

    'updates': {
        'lines': [{
            'name': 'Strong Line',
            'probability': 1.1,
            'price': 500,
        }, {
            'name': 'Braided Line',
            'probability': 1.2,
            'price': 1000,
        }],
        'boats': [{
            'name': 'Row Boat',
            'time': -5,
            'price': 1000,
        }, {
            'name': 'Motor Boat',
            'time': -10,
            'price': 3000,
        }, {
            'name': 'Speed Boat',
            'time': -15,
            'price': 7000,
        }],
        'cues': [{
            'name': 'A Map',
            'cueDetail': 1,
            'price': 50,
        }, {
            'name': 'Underwater Camera',
            'cueDetail': 2,
            'price': 200,
        }, {
            'name': 'Old Sonar',
            'cueDetail': 3,
            'price': 4000,
        }, {
            'name': 'Modern Sonar',
            'cueDetail': 4,
            'price': 10000,
        }, {
            'name': 'A Mermaid',
            'cueDetail': 5,
            'price': 30000,
        }],
    },

    'modifiers': {
        'worm': {
            'bass': 1.2,
            'brime': 1.5,
            'price': 200,
        },
        'spinner': {
            'pike': 1.3,
            'brime': 0.8,
            'price': 200,
        },
        'vobbler': {
            'brime': 0.5,
            'pike': 1.4,
            'catfish': 1.2,
            'price': 2000,
        }
    },

    'levels': [{
        'name': 'Local pond',
        'fish': {
            'shoe': {
                'probability': 0.7,
                'distribution': {
                    'type': 'uniform-declining',
                    'options': {
                        'zero-at': 20,
                    },
                },
            },
            'bass': {
                'probability': 0.3,
                'distribution': {
                    'type': 'uniform-declining',
                    'options': {
                        'zero-at': 10,
                    },
                },
            },
        },
        'cost': 0,
        'timesToPlay': 4,
        'mean': 35.0,
        'std': 3.7,
      }, {
        'name': 'Lake',
        'fish': {
            'bass': {
                'probability': 0.6,
                'distribution': {
                    'type': 'uniform-declining',
                    'options': {
                        'zero-at': 15,
                    },
                },
            },
            'brime': {
                'probability': 0.4,
                'distribution': {
                    'type': 'uniform-declining',
                    'options': {
                        'zero-at': 10,
                    },
                },
            },
            'pike': {
                'probability': 0.3,
                'distribution': {
                    'type': 'nth-declining',
                    'options': {
                        'n': 3,
                        'zero-at-n': 10,
                    },
                },
            },
        },
        'cost': 120,
        'timesToPlay': 5,
        'mean': 166.0,
        'std': 16.0,
      }, {
        'name': 'River',
        'fish': {
            'bass': {
                'probability': 0.7,
                'distribution': {
                    'type': 'uniform-declining',
                    'options': {
                        'zero-at': 15,
                    },
                },
            },
            'pike': {
                'probability': 0.3,
                'distribution': {
                    'type': 'nth-declining',
                    'options': {
                        'n': 3,
                        'zero-at-n': 10,
                    },
                },
            },
            'catfish': {
                'probability': 0.2,
                'distribution': {
                    'type': 'nth-constant',
                    'options': {
                        'n': 7,
                        'val': 1.0,
                    },
                },
            },
        },
        'cost': 740,
        'timesToPlay': 6,
        'mean': 351.0,
        'std': 64.0,
    }],
}

# a function to get the fish for this level
def getFishForLevel(level):
    f = {}
    for fish, locF in GAME['levels'][level]['fish'].iteritems():
        newFish = dict(GAME['fish'][fish])
        newFish['probability'] = locF['probability']
        newFish['distribution'] = locF['distribution']
        f[fish] = newFish
    return f

# a function to get the level dict
def getLevel(level):
    lvl = dict(GAME['levels'][level])
    lvl['index'] = level
    lvl['time'] = 0
    lvl['totalTime'] = TOTAL_TIME
    lvl['map'] = maps.generate(maxDepth=10, width=20)
    lvl['position'] = 0

    # time spent in each location
    lvl['timeInLoc'] = [0 for i in range(20)]

    # yields are not yet defined
    lvl['yields'] = [None for i in range(20)]

    return lvl

