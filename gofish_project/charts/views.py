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
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('charts/data_user.html', context_dict, context)

@user_passes_test(lambda u: u.is_superuser)
def dataAggregated(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('charts/data_aggregated.html', context_dict, context)

@user_passes_test(lambda u: u.is_superuser)
def getData(request):
    response = {
            'xName': 'Moves',
            'yName': 'Divergence from Optimum',
            'rows' : [ [1, 3], [2, 2], [3, 1], [4, -1], [5, 0] ],
            'title': 'How Optimal was the Amount of Time Spent in Location'
    }
    return HttpResponse(json.dumps(response), content_type="application/json")
