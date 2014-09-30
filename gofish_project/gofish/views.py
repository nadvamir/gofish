from django.http import HttpResponse
import json

def index(request):
    return HttpResponse("Gofish says hello world!")

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
