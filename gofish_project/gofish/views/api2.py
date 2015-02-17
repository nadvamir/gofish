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
        # star scores
        stars = player.getAchievement('moneyIn' + str(i))
        stars = stars.rating if None != stars else 0
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
            'stars'    : stars
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
    player   = models.Player.initialise(request.user)
    response['trophies'] = {}

    for fish in response['fish'].keys():
        trophy = player.getAchievement(fish)
        trophy = trophy.toDict() if None != trophy else {'value': 0.0, 'rating': 0}
        response['trophies'][fish] = trophy

    return HttpResponse(json.dumps(response), content_type="application/json")

################################################################
# Helpers
################################################################
# get index for a player update
def getIndex(player, update):
    return -1 if update not in player.updates else gamedef.getIndex(player.updates[update], update)

