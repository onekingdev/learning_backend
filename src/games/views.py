import json

from django.http import HttpResponse
from django.core.files import File
from django.conf import settings
import lxml.html as LH
from graphql_jwt.utils import jwt_decode
from django.contrib.auth import get_user_model
from games.models import Game
import os
import lxml.html as LH

User = get_user_model()

def crud(request, folder_name):
    token = request.GET['token'];
    print(request)
    id = ""
    contents = "Game Not Found!"
    game = ""
    path = ""
    # --------------------- Get user and game from DB -S--------------------------#
    try:
        payload = jwt_decode(token)
        id = payload['sub']
        game = Game.objects.get(path = folder_name)
        path = settings.MEDIA_ROOT + "games/" + game.path + "/" + game.random_slug+"_index.html"
    except Exception as e:
        return HttpResponse(contents)
    # --------------------- Get user and game from DB -E--------------------------#
    
    # --------------- Change the index.html file name to randomg slug name -S----------------#    
    if not os.path.exists(path) :
        initial_path = settings.MEDIA_ROOT + "games/" + game.path + "/"
        if os.path.exists(initial_path + "index.html") :
            initial_path = initial_path + "index.html"
        elif os.path.exists(initial_path + "index.htm") :
            initial_path = initial_path + "index.html"
        else : 
            return HttpResponse(contents)
        os.rename(initial_path, path)
    # --------------- Change the file name  (index.html) to randomg slug name -E----------------#  

    # --------------- Read Content of index.html file -S---------------------#
    file = open(path, 'r')
    contents =file.read()
    # --------------- Read Content of index.html file -E---------------------#   

    if( not id or not contents) :
        contents = "Game Not Found!"
    return HttpResponse(contents)