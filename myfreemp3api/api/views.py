from ast import Delete
from http.client import HTTPResponse
import logging
from mutagen.easyid3 import EasyID3

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
import django.views.defaults

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

@api_view(['GET'])
def song_list(request):
    try:
        songDBs = SongDB.objects.filter(user=request.user)
        songDBsSerializer = SongDBSerializer(songDBs, many=True, context={'request': request})
        songDBsData = list(songDBsSerializer.data)        
        return get_json_response_paginated(request, songDBsData)

    except SongDB.DoesNotExist as exception:
        return django.views.defaults.page_not_found(request=request, exception=exception)

@api_view(['GET', 'PUT', 'DELETE'])
def song_detail(request, pk):
    try:
        songDB = SongDB.objects.get(pk=pk)
    except SongDB.DoesNotExist as exception:
        return django.views.defaults.page_not_found(request=request, exception=exception)

    songDBSerializer = SongDBSerializer(songDB, data=request.data)

    if songDBSerializer.is_valid():

        if request.method == 'GET':
            return JsonResponse(songDBSerializer.data)

        if request.method == 'PUT':
            songDBSerializer.save()
            songFile = EasyID3(songDB.path)
            if songDB.title is None:
                songDB.title = ""
            songFile[apiSettings.ID3_TAG_TITLE] = songDB.title
            if songDB.artist is None:
                songDB.artist = ""
            songFile[apiSettings.ID3_TAG_ARTIST] = songDB.artist
            if songDB.album is None:
                songDB.album = ""
            songFile[apiSettings.ID3_TAG_ALBUM] = songDB.album 
            if songDB.genre is None:
                songDB.genre = ""
            songFile[apiSettings.ID3_TAG_GENRE] = songDB.genre 
            if songDB.rating is None:
                songDB.rating = 0
            songFile[apiSettings.ID3_TAG_RATING] = str(songDB.rating)
            if songDB.language is None:
                songDB.language = ""
            songFile[apiSettings.ID3_TAG_LANGUAGE] = songDB.language
            songFile.save()

            return JsonResponse(songDBSerializer.data)

        if request.method == 'DELETE':
            songDB.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    return JsonResponse(songDBSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class ExternalSongsView(generics.ListAPIView):

    def list(self, request):
        if request.GET.get(apiSettings.FIELD_SOURCE, False) == apiSettings.EXTERNAL_SOURCE_MYFREEMP3:
            query = request.GET.get(apiSettings.FIELD_QUERY, False)
            pageNumber = request.GET.get(apiSettings.FIELD_PAGE, 0)
            externalSongs = myfreemp3scrapper.scrap(query, pageNumber)
            paginator = Paginator(externalSongs, PageNumberPagination.page_size)
            page_object = paginator.get_page(pageNumber)
            return get_json_response_paginated(request, externalSongs)
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

def get_json_response_paginated(request, dataJsonList):

    pageNumber = request.GET.get(apiSettings.FIELD_PAGE, 0)
    paginator = Paginator(dataJsonList, PageNumberPagination.page_size)
    page_object = paginator.get_page(pageNumber)

    return JsonResponse({
        "count": len(dataJsonList),
        "current": pageNumber,
        "next": page_object.has_next(),
        "previous": page_object.has_previous(),
        "data": dataJsonList
    })