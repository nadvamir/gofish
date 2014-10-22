from random import randint
from math import floor
from random import gauss
from random import random

STEP_SIZE = 5 # 12 fish per hour max

# a yield function returns a list of fish one can catch
# there is a maximum of 12 fish per hour, and it is the
# value of the caught fish that is being rigged

#################################################################
# HELPERS
#################################################################
# a function that gives a specific instance of a fish
def catch(fish):
    # let's say that 1 SD is 25 percent of median
    caught = {
        'name': fish['name'],
        'weight': gauss(fish['weight'], fish['weight'] * 0.25),
        'length': gauss(fish['length'], fish['length'] * 0.25),
    }
    caught['value'] = round(caught['weight'] / fish['weight'] * fish['value'])
    return caught

# a function to catch a fish only when you are lucky enough
def catchIfYouCan(fish):
    if random() <= fish['probability']:
        return catch(fish)
    return None

# a function to select which fish to try to catch
# the more likely you are to catch it, the more likely
# will you select one
def chooseFish(fishList):
    total = 0
    for fish in fishList:
        total += fish['probability']

    rnd = random()
    for fish in fishList:
        if rnd <= fish['probability'] / total:
            return fish
        else:
            rnd -= fish['probability'] / total

    return fishList[len(fishList) - 1]

#################################################################
# YIELDS
#################################################################
# a really constant yield
def getConstantYield(totalTime, fish):
    maxFish = totalTime / STEP_SIZE
    caught = []
    for i in range(maxFish):
        caught.append({
            name   : fish['name'],
            weight : fish['weight'],
            length : fish['length'],
            value  : fish['value'],
        })
    return caught


# a yield that tries to match the target, if possible,
# over the whole spectrum
def getTargetYield(totalTime, target, fishList):
    caught = []
    maxFish = totalTime / STEP_SIZE

    # catch the required ammount of fish
    value = 0
    while value < target and len(caught) < maxFish:
        fish = catchIfYouCan(chooseFish(fishList))
        caught.append(fish)
        if None != fish:
            value += fish['value']

    for i in range(len(caught), maxFish):
        caught.append(None)
    
    return caught

# a completely random yield
def getRandomYield(totalTime, fishList):
    maxFish = totalTime / STEP_SIZE
    return [catchIfYouCan(chooseFish(fishList)) for i in range(maxFish)]

