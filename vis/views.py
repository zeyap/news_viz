from django.http import HttpResponse

def index(request):
    return HttpResponse("{'message':'Hello, world. You're at the visualization index.'}")