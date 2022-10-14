from mutagen.easyid3 import EasyID3

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator

from .serializers import UserSerializer, GroupSerializer, SongDBSerializer

import myfreemp3api.api.settings as apiSettings
import myfreemp3api.api.controller.externalSongDownloadController as externalSongDownloadController
from myfreemp3api.model.externalsong import ExternalSong
from myfreemp3api.models import SongDB
import myfreemp3api.myfreemp3scrapper.scrapper as myfreemp3scrapper

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class SongDBViewSet(viewsets.ModelViewSet):
    serializer_class = SongDBSerializer

    def get_queryset(self):
        return SongDB.objects.filter(user=self.request.user)

@api_view(['GET', 'PUT', 'DELETE'])
def song_detail(request, pk):
    try:
        song = SongDB.objects.get(pk=pk)
    except song.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    songDBSerializer = SongDBSerializer(song, data=request.data)

    if request.method == 'GET':
        if songDBSerializer.is_valid():
            return JsonResponse(songDBSerializer.data)
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        if songDBSerializer.is_valid():
            songDBSerializer.save()
            songFile = EasyID3(song.path)
            if song.title is None:
                song.title = ""
            songFile[apiSettings.ID3_TAG_TITLE] = song.title
            if song.artist is None:
                song.artist = ""
            songFile[apiSettings.ID3_TAG_ARTIST] = song.artist
            if song.album is None:
                song.album = ""
            songFile[apiSettings.ID3_TAG_ALBUM] = song.album 
            if song.genre is None:
                song.genre = ""
            songFile[apiSettings.ID3_TAG_GENRE] = song.genre 
            if song.rating is None:
                song.rating = 0
            songFile[apiSettings.ID3_TAG_RATING] = str(song.rating)
            if song.language is None:
                song.language = ""
            songFile[apiSettings.ID3_TAG_LANGUAGE] = song.language
            songFile.save()
            return JsonResponse(songDBSerializer.data)
        return JsonResponse(songDBSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class ExternalSongsView(generics.ListAPIView):

    def list(self, request):
        if request.GET.get(apiSettings.FIELD_SOURCE, False) == apiSettings.EXTERNAL_SOURCE_MYFREEMP3:
            query = request.GET.get(apiSettings.FIELD_QUERY, False)
            pageNumber = request.GET.get(apiSettings.FIELD_PAGE, 0)
            externalSongs = myfreemp3scrapper.scrap(query, pageNumber)
            paginator = Paginator(externalSongs, PageNumberPagination.page_size)
            page_object = paginator.get_page(pageNumber)
            payload = {
                "count": len(externalSongs),
                "current": pageNumber,
                "next": page_object.has_next(),
                "previous": page_object.has_previous(),
                "data": externalSongs
            }
            return JsonResponse(payload)
        else:
            return JsonResponse(
                {
                    apiSettings.FIELD_STATUS :'false',
                    apiSettings.FIELD_DURATION : apiSettings.EXTERNAL_SOURCE_DOESNT_EXIST_MESSAGE
                }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class ExternalSongDownloadView(APIView):
 
    def post(self, request):
        externalSongUrl = request.POST[apiSettings.FIELD_EXTERNAL_SONG_URL]
        title = request.POST[apiSettings.FIELD_TITLE]
        artist = request.POST[apiSettings.FIELD_ARTIST]
        date = request.POST[apiSettings.FIELD_DATE]
        externalSong = ExternalSong(title, artist, None, date, externalSongUrl)
        songDB = externalSongDownloadController.downloadExternalSong(request.user, externalSong)
        songDBSerializer = SongDBSerializer(songDB, data = request.data)
        if songDBSerializer.is_valid():
            return JsonResponse(songDBSerializer.data)
        else:
            return JsonResponse(songDBSerializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def UserCreationView(request):
    if (request.method == "POST"):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        userId = userCreationController.CreateUser(name, email, password)
        return HttpResponseRedirect(str(userId))