from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
import json

from models import DataPoint

#################################################################
# CHART ADMIN
#################################################################
@user_passes_test(lambda u: u.is_superuser)
def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    context_dict = {}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('charts/index.html', context_dict, context)

@user_passes_test(lambda u: u.is_superuser)
def parseLog(request):
    numEntries = 0
    # parse the log file
    with open('gofish.log', 'r') as f:
        for line in f:
            if line != '\n':
                DataPoint.insertFromLine(line)
                numEntries += 1

    # flush the log file
    with open('gofish.log', 'w') as f:
        pass

    # report on the number of processed lines
    context = RequestContext(request)
    context_dict = {'numEntries': numEntries}
    return render_to_response('charts/log_parsed.html', context_dict, context)

@user_passes_test(lambda u: u.is_superuser)
def dataByUser(request):
    choices = DataPoint.describeData()
    context = RequestContext(request)
    context_dict = {'choices': choices}
    return render_to_response('charts/data_user.html', context_dict, context)

@user_passes_test(lambda u: u.is_superuser)
def dataAggregated(request):
    context = RequestContext(request)
    context_dict = {
        'choices': {
            'bar': {
                'optTime'      : 'Optimality of Time',
                'optMoney'     : 'Optimality of Money',
                'loptTime'     : 'Local Opt. of Time',
                'loptMoney'    : 'Local Opt. of Money',
                'optTimeAbs'   : 'Absolute Opt. of Time',
                'optMoneyAbs'  : 'Absolute Opt. of Money',
                'loptTimeAbs'  : 'Absolute Loc. Opt. of Time',
                'loptMoneyAbs' : 'Absolute Loc. Opt. of Money'
            },
            'boxX': {
                'cueDetail'    : 'Detail of Cues',
                'level'        : 'Level of Game',
                'gameNum'      : 'Game Number',
                'fishCost'     : 'Fishing Cost',
                'moveCost'     : 'Moving Cost',
                'endGame'      : 'End Game',
                'level'        : 'Level of Game',
            },
            'boxY': {
                'optTime'      : 'Optimality of Time',
                'optMoney'     : 'Optimality of Money',
                'loptTime'     : 'Local Opt. of Time',
                'loptMoney'    : 'Local Opt. of Money',
                'optTimeAbs'   : 'Absolute Opt. of Time',
                'optMoneyAbs'  : 'Absolute Opt. of Money',
                'loptTimeAbs'  : 'Absolute Loc. Opt. of Time',
                'loptMoneyAbs' : 'Absolute Loc. Opt. of Money'
            }
        }
    }
    return render_to_response('charts/data_aggregated.html', context_dict, context)

#################################################################
# Optimisation of the Game
#################################################################
@user_passes_test(lambda u: u.is_superuser)
def optimise(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('charts/optimise.html', context_dict, context)

#################################################################
# Data API
#################################################################
# data for single user query
@user_passes_test(lambda u: u.is_superuser)
def getData(request):
    qs = DataPoint.query(
        username  = request.GET.get('username', None),
        gameNum   = request.GET.get('gameNum', None),
        cueDetail = request.GET.get('cueDetail', None),
        level     = request.GET.get('level', None),
        moveCost  = request.GET.get('moveCost', None),
        endGame   = request.GET.get('endGame', None))

    response = {'data': [el.toDict() for el in qs]}
    return HttpResponse(json.dumps(response), content_type="application/json")

# data for aggregated bar charts 
@user_passes_test(lambda u: u.is_superuser)
def getBarData(request):
    qs = DataPoint.queryBarData(request.GET.get('x', None))

    response = {'data': [el for el in qs]}
    return HttpResponse(json.dumps(response), content_type="application/json")

# data for aggregated box charts
@user_passes_test(lambda u: u.is_superuser)
def getBoxData(request):
    qs = DataPoint.queryBoxData(
        x = request.GET.get('x', None),
        y = request.GET.get('y', None))

    response = {'data': [el for el in qs]}
    return HttpResponse(json.dumps(response), content_type="application/json")

