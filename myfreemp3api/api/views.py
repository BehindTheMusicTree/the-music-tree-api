from django.contrib.auth.models import User, Group
from myfreemp3api.api.models import *
from rest_framework import viewsets
from .serializers import *
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import json
from myfreemp3api.scrapper import myfreemp3_scrapper

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

def SongView(request):
    if (request.method == "GET"):
        # return JsonResponse(json.loads("""
        # {\"count\": 2,
        # \"results\": 
        # [
        #     {\"name\": \"Trauma\", \"author\": \"Nto\"},
        #     {\"name\": \"Africa\", \"author\": \"Toto\"}
        # ]}
        # """), safe=False)
        return JsonResponse(myfreemp3_scrapper.scrap(), safe=False)