from .serializers import *

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponseRedirect

import myfreemp3api.api.settings as apiSettings
import myfreemp3api.myfreemp3scrapper.scrapper as myfreemp3scrapper
import myfreemp3api.api.controller.externalSongDownloadController as externalSongDownloadController
from myfreemp3api.model.song import Song

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
 
class SongsExternalView(APIView):
 
    def get(self, request):
        if request.GET.get(apiSettings.FIELD_SOURCE, False) == apiSettings.EXTERNAL_SOURCE_MYFREEMP3:
            query = request.GET.get(apiSettings.FIELD_QUERY, False)
            return JsonResponse(myfreemp3scrapper.scrap (query), safe = False)
        else:
            return JsonResponse(
                {
                    apiSettings.FIELD_STATUS :'false',
                    apiSettings.FIELD_DURATION : apiSettings.EXTERNAL_SOURCE_DOESNT_EXIST_MESSAGE
                }, status = 500)
 
class ExternalSongDownloadView(APIView):
 
    def post(self, request):
        externalSongUrl = request.POST[apiSettings.FIELD_EXTERNAL_SONG_URL]
        title = request.POST[apiSettings.FIELD_TITLE]
        artist = request.POST[apiSettings.FIELD_ARTIST]
        date = request.POST[apiSettings.FIELD_DATE]
        song = Song(title, artist, None, date, externalSongUrl)
        externalSongDownloadController.downloadExternalSong(request.user, song)
        return JsonResponse({'url': externalSongUrl}, safe = False)

@api_view(['POST'])
def UserCreationView(request):
    if (request.method == "POST"):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        userId = userCreationController.CreateUser(name, email, password)
        return HttpResponseRedirect(str(userId))