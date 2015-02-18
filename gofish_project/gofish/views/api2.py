from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response
from lazysignup.decorators import allow_lazy_user
import json

import gofish.models as models
import gofish.engine.gamedef as gamedef

#################################################################
# API v2
#################################################################
# get the information about the levels
@allow_lazy_user
def v2home(request):
    player   = models.Player.initialise(request.user)
    response = {'levels': []}

    for i in range(len(gamedef.GAME['levels'])):
        # star scores for player
        record = player.getAchievement('moneyIn' + str(i))
        stars = record.rating if None != record else 0
        highS = record.value if None != record else 0
        # highest scores for everyone
        records = models.Achievement.getTop('moneyIn' + str(i))
        maxHighS = records[0].value if 0 != len(records) else 0
        # other parameters
        unlocked = player.level >= i
        active = player.level + 1 >= i
        # putting it all together
        response['levels'].append({
            'id'       : i,
            'name'     : gamedef.GAME['levels'][i]['name'],
            'unlocked' : unlocked,
            'active'   : active,
            'cost'     : gamedef.GAME['levels'][i]['cost'],
            'stars'    : stars,
            'highS'    : highS,
            'maxHighS' : maxHighS,
        })

    return HttpResponse(json.dumps(response), content_type="application/json")

# get the information about the player
@allow_lazy_user
def v2player(request):
    player   = models.Player.initialise(request.user)
    response = {'player': {
        'money' : player.money,
        'boat'  : getIndex(player, 'boats'),
        'line'  : getIndex(player, 'lines'),
        'cue'   : getIndex(player, 'cues'),
    }}
    return HttpResponse(json.dumps(response), content_type="application/json")

# get the information about the active game
@allow_lazy_user
def v2game(request):
    player = models.Player.initialise(request.user)
    game   = models.Game.initialise(player)
    if None == game:
        return HttpResponseNotFound()

    caught = reduce(lambda a, f: a + f['value'], game.caught, 0)
    response = {'game' : {
        'day'       : player.numGames,
        'name'      : game.level['name'],
        'totalTime' : game.level['totalTime'],
        'timeLeft'  : game.level['totalTime']-game.level['time'],
        'valCaught' : caught,
        'showDepth' : 'cues' in player.updates,
        'map'       : game.level['map'],
        'position'  : game.level['position'],
        'cues'      : game.getCues(),
        'caught'    : game.caught,
    }}

    return HttpResponse(json.dumps(response), content_type="application/json")

# get the trophies
@allow_lazy_user
def v2trophies(request):
    player = models.Player.initialise(request.user)
    response['trophies'] = {}

    for fish in response['fish'].keys():
        trophy = player.getAchievement(fish)
        trophy = trophy.toDict() if None != trophy else {'value': 0.0, 'rating': 0}
        response['trophies'][fish] = trophy

    return HttpResponse(json.dumps(response), content_type="application/json")

# get the shop items
@allow_lazy_user
def v2shop(request):
    response = {
        'boats' : [],
        'lines' : [],
        'cues'  : []
    }

    # add a default boat
    response['boats'].append({
        'name' : 'Raft',
        'cost' : 0,
        'perk' : 'It floats.'
    })
    # add a default line
    response['lines'].append({
        'name' : 'Old Fishing Line',
        'cost' : 0,
        'perk' : 'You\'ve found it in the attic.'
    })
    # add a default queue
    response['cues'].append({
        'name' : 'Your Eyes',
        'cost' : 0,
        'perk' : 'You can\'t quite see underwater...'
    })

    # build boats
    for boat in gamedef.GAME['updates']['boats']:
        response['boats'].append({
            'name' : boat['name'],
            'cost' : boat['price'],
            'perk' : 'It is ' + str(boat['time'] / (-5) * 16) + ' % faster!'
        })

    # build lines
    for line in gamedef.GAME['updates']['lines']:
        response['lines'].append({
            'name' : line['name'],
            'cost' : line['price'],
            'perk' : str(line['probability'] * 100 - 100) + ' % more fish!'
        })

    # build cues
    cues = gamedef.GAME['updates']['cues']
    response['cues'].append({
        'name' : cues[0]['name'],
        'cost' : cues[0]['price'],
        'perk' : 'It shows you how deep water is'
    })
    for i in range(1, len(cues)):
        response['cues'].append({
            'name' : cues[i]['name'],
            'cost' : cues[i]['price'],
            'perk' : 'It tells you the fish under you with the accuracy of ' + str(cues[i]['accuracy']) + ' %'
        })

    return HttpResponse(json.dumps(response), content_type="application/json")

################################################################
# Helpers
################################################################
# get index for a player update
def getIndex(player, update):
    return -1 if update not in player.updates else gamedef.getIndex(player.updates[update], update)

