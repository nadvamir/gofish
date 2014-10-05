from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import json

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    context_dict = {}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('gofish/index.html', context_dict, context)

def start(request, level):
    response = {'level': level}
    return HttpResponse(json.dumps(response), content_type="application/json")

def end(request):
    response = {}
    return HttpResponse(json.dumps(response), content_type="application/json")

def action(request, action, par):
    response = {'action': action, 'par': par}
    return HttpResponse(json.dumps(response), content_type="application/json")

def update(request, target):
    response = {'target': target}
    return HttpResponse(json.dumps(response), content_type="application/json")

def choose(request, modifier):
    response = {'modifier': modifier}
    return HttpResponse(json.dumps(response), content_type="application/json")

def buy(request, modifier):
    response = {'modifier': modifier}
    return HttpResponse(json.dumps(response), content_type="application/json")

def getgame(request):
    response = {}
    return HttpResponse(json.dumps(response), content_type="application/json")
