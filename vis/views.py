from django.http import HttpResponse
from django.contrib.auth import authenticate
import json

def index(request):
    username = request.POST.get('username','anonymous')
    password = request.POST.get('password','null')
    user = authenticate(request, username = username, password = password)
    # print(user,username,password)
    if user is not None:
        resp = {'message':"Hello, world. You're at the visualization index."}
        return  HttpResponse(json.dumps(resp),content_type="application/json")
    else:
        resp = {'errorcode':500, 'detail':'invalid user'}
        return  HttpResponse(json.dumps(resp),content_type="application/json")