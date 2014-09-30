from django.http import HttpResponse

def index(request):
    return HttpResponse("Gofish says hello world!")
