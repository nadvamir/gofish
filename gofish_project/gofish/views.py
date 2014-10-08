from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from lazysignup.decorators import allow_lazy_user
import json
import models

#################################################################
# WEBSITE
#################################################################
@allow_lazy_user
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

@allow_lazy_user
def levelselect(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('gofish/levelselect.html', context_dict, context)

@allow_lazy_user
def shop(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('gofish/shop.html', context_dict, context)

@allow_lazy_user
def level(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('gofish/level.html', context_dict, context)

@allow_lazy_user
def results(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('gofish/results.html', context_dict, context)

#################################################################
# API
#################################################################
@allow_lazy_user
def start(request, level):
    response = {'level': level}
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def end(request):
    response = {}
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def action(request, action, par):
    response = {'action': action, 'par': par}
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def update(request, target):
    response = {'target': target}
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def choose(request, modifier):
    response = {'modifier': modifier}
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def buy(request, modifier):
    response = {'modifier': modifier}
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def getgame(request):
    player = models.Player.initialise(request.user)
    response = {'user': player.__unicode__(),
                'money': player.money}
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def getmodifiers(request):
    response = {}
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def getupdates(request):
    response = {}
    return HttpResponse(json.dumps(response), content_type="application/json")
