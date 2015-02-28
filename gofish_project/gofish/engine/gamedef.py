import maps

# here we have a GAME definition object, already priced
TOTAL_TIME = 480
FISHING_COST = 5
MOVE_COST = 60
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
            'name': 'Bream',
            'value': 29,
            'weight': 1.0,
            'length': 40,
            'habitat': 6,
        },
        'pike': {
            'id': 'pike',
            'name': 'Pike',
            'value': 70,
            'weight': 1.5,
            'length': 50,
            'habitat': 3,
        },
        'catfish': {
            'id': 'catfish',
            'name': 'Catfish',
            'value': 300,
            'weight': 10.0,
            'length': 100,
            'habitat': 9,
        },
        'cod': {
            'id': 'cod',
            'name': 'Cod',
            'value': 200,
            'weight': 10.0,
            'length': 100,
            'habitat': 9,
        },
        'tuna': {
            'id': 'tuna',
            'name': 'Tuna',
            'value': 1000,
            'weight': 20.0,
            'length': 110,
            'habitat': 9,
        },
        'carp': {
            'id': 'carp',
            'name': 'Salmon',
            'value': 290,
            'weight': 7.0,
            'length': 70,
            'habitat': 5,
        },
    },

    'updates': {
        'lines': [{
            'name': 'Strong Line',
            'probability': 1.1,
            'price': 1000,
        }, {
            'name': 'Braided Line',
            'probability': 1.2,
            'price': 2000,
        }],
        'boats': [{
            'name': 'Row Boat',
            'time': -20,
            'price': 500,
        }, {
            'name': 'Motor Boat',
            'time': -40,
            'price': 6000,
        }, {
            'name': 'Speed Boat',
            'time': -50,
            'price': 24000,
        }],
        'cues': [{
            'name': 'A Map',
            'cueDetail': 1,
            'price': 30,
            'depth': 0,
            'accuracy': 0,
        }, {
            'name': 'Underwater Camera',
            'cueDetail': 2,
            'price': 350,
            'depth': 4,
            'accuracy': 50,
        }, {
            'name': 'Old Sonar',
            'cueDetail': 3,
            'price': 1000,
            'depth': 7,
            'accuracy': 70,
        }, {
            'name': 'Modern Sonar',
            'cueDetail': 4,
            'price': 6200,
            'depth': 10,
            'accuracy': 85,
        }, {
            'name': 'A Mermaid',
            'cueDetail': 5,
            'price': 30000,
            'depth': 10,
            'accuracy': 100,
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
            'price': 200,
        },
        'jig': {
            'brime': 0.5,
            'pike': 0.5,
            'perch': 1.2,
            'tuna': 1.5,
            'cod': 1.5,
            'price': 5000,
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
        'maxDepth': 4,
        'timesToPlay': 3,
        'mean': 30.0,
        'std': 2.5,
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
        'cost': 90,
        'maxDepth': 6,
        'timesToPlay': 3,
        'mean': 350.0,
        'std': 45.0,
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
        'cost': 1050,
        'maxDepth': 9,
        'timesToPlay': 4,
        'mean': 500.0,
        'std': 90.0,
      }, {
        'name': 'Sea',
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
            'cod': {
                'probability': 0.7,
                'distribution': {
                    'type': 'uniform-declining',
                    'options': {
                        'zero-at': 30,
                    },
                },
            },
            'tuna': {
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
        'cost': 2000,
        'maxDepth': 9,
        'timesToPlay': 5,
        'mean': 6200.0,
        'std': 470.0,
      }, {
        'name': 'Salmon Farm',
        'fish': {
            'carp': {
                'probability': 0.7,
                'distribution': {
                    'type': 'uniform-random',
                    'options': {
                        'lower': 0.0,
                        'upper': 1.0,
                    },
                },
            },
            'pike': {
                'probability': 0.2,
                'distribution': {
                    'type': 'nth-declining',
                    'options': {
                        'n': 3,
                        'zero-at-n': 10,
                    },
                },
            },
        },
        'cost': 31000,
        'maxDepth': 9,
        'timesToPlay': 6,
        'mean': 7500.0,
        'std': 300.0,
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
    lvl['map'] = maps.generate(maxDepth=(lvl['maxDepth'] + 1), width=20)
    lvl['position'] = 0

    # time spent in each location
    lvl['timeInLoc'] = [0 for i in range(20)]

    # yields are not yet defined
    lvl['yields'] = [None for i in range(20)]

    return lvl

# a function to get index for an update
def getIndex(name, update):
    for i in range(0, len(GAME['updates'][update])):
        if GAME['updates'][update][i]['name'] == name:
            return i
    return -1

