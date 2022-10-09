from .serializers import *

import logging

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponseRedirect

from myfreemp3api.api.models import *
from myfreemp3api.api.configuration import configuration
from myfreemp3api.myfreemp3_scrapper import scrapper
from myfreemp3api.api.controller.songExternalDownloadController import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
 
class SongsExternalView(APIView):
 
    def get(self, request):
        if request.GET.get('source', False) == configuration["externalSourceMyfreemp3"]:
            return JsonResponse(scrapper.scrap(request.GET.get('query', False)), safe = False)
        else:
            return JsonResponse(
                {
                    'status':'false',
                    'message': configuration["externalSourceDoesntExistMessage"]
                }, status=500)
 
class SongsExternalDownloadView(APIView):
 
    def post(self, request):
        songExternalUrl = request.POST['songUrl']
        logger = logging.getLogger("info")
        logger.info("auth header : " + request.META['HTTP_AUTHORIZATION'])
        downloadExternalSong(request.user, songExternalUrl)
        return JsonResponse({'url': songExternalUrl}, safe = False)

@api_view(['POST'])
def UserCreationView(request):
    if (request.method == "POST"):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        userId = userCreationController.CreateUser(name, email, password)
        return HttpResponseRedirect(str(userId))