from random import uniform
from random import random
from random import randint
import gamedef

generators = [
    lambda g, p: createNoCue(),             # no cues
    lambda g, p: createCue(g, p, -1, 0.1),  # map
    lambda g, p: createCue(g, p, 5, 0.5),   # camera
    lambda g, p: createCue(g, p, 8, 0.7),   # old sonar
    lambda g, p: createCue(g, p, 10, 0.85), # modern sonar
    lambda g, p: createCue(g, p, 10, 1.0)   # mermaid
]

#################################################################
# INTERFACE
#################################################################
# function to generate the cues
def generate(game, position):
    # get the level of detail
    detail = game.player.getCueDetail()
    # create a specific cue for that level of detail
    return generators[detail](game, position)

#################################################################
# INTERNALS
#################################################################
# creates a cue that does not show anything
def createNoCue():
    return [[-1, 0]]

# creates a cue with some information
# all of the cues here know at least te depth
# visibility: how many metres down can it see
# accuracy: how accurate are the predictions
# return format: a list of lists for every depth unit
#   in a format [number of fish, the size indication]]
def createCue(game, pos, visibility, accuracy):
    fish = getFish(game, pos)
    maxDepth = game.level['map'][0][pos]
    cues = []
    for i in range(0, maxDepth):
        cues.append(aggregateFish(fish, i, visibility,
                                  accuracy, maxDepth - 1))
    return cues

# a function that returns the list of fishes in the yield
def getFish(game, pos):
    fish = {}
    # initial list
    yields = game.level['yields'][pos]
    for i in range(game.level['timeInLoc'][pos], len(yields)):
        if None != yields[i]:
            addFish(fish, yields[i])

    # add prefered depth
    for k, v in fish.iteritems():
        v['depth'] = getDepth(k)

    return fish

# adds fish to a fish list
def addFish(fishList, fish):
    if fish['name'] not in fishList:
        fishList[fish['name']] = {'weight': 0.0, 'count': 0}
    fishList[fish['name']]['weight'] += fish['weight']
    fishList[fish['name']]['count'] += 1

# a function that gets the preferred depth of a fish
def getDepth(fishName):
    for k, v in gamedef.GAME['fish'].iteritems():
        if fishName == v['name']:
            return v['habitat']
    return -1

# a function that aggregates all the fish on that depth
def aggregateFish(fish, depth, visibility, accuracy, mdepth):
    # if it is deeper than we see, we have no info:
    if depth > visibility:
        return [-1, 0]

    # calculate average weight and total count of fish here
    weight = 0.0
    count = 0.0
    for k, v in fish.iteritems():
        if v['depth'] == depth or depth == mdepth and v['depth'] > depth:
            weight += v['weight']
            count += v['count']
    if count > 0:
        weight /= count

    # introducing error with respect to accuracy
    count = round(uniform(count * accuracy, count / accuracy))
    weight = uniform(weight * accuracy, weight / accuracy)
    # ghost sygnals
    if random() > accuracy:
        count += randint(0, 2)
        weight += random()

    # calculating size indicator
    indicator = 0
    if weight > 0.5 and weight <= 1.0:
        indicator = 1
    elif weight > 1.0 and weight <= 3.0:
        indicator = 2
    elif weight > 3.0 and weight <= 10.0:
        indicator = 3
    else:
        indicator = 4

    return [count, indicator]
