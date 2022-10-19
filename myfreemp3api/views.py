from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
import django.views.defaults

from .serializers import UserSerializer, GroupSerializer, SongDBSerializer

import myfreemp3api.api.settings as apiSettings
import myfreemp3api.api.controller.externalSongDownloadController as externalSongDownloadController
from myfreemp3api.models import ExternalSong
from myfreemp3api.models import SongDB

from myfreemp3api.dao.LibrarySongDAO import LibrarySongDAO
from myfreemp3api.dao.ExternalSongMyfreemp3DAO import ExternalSongMyfreemp3DAO

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

    if request.method == 'GET':
        try:
            songDB = LibrarySongDAO.get(pk)
            songDBSerializer = SongDBSerializer(songDB, context={'request': request})
            return JsonResponse(songDBSerializer.data)
        except SongDB.DoesNotExist as exception:
            return django.views.defaults.page_not_found(request=request, exception=exception)

    if request.method == 'PUT':        
        try:
            songDBUpdated = LibrarySongDAO.update(
                songId=pk,
                title=request.data[apiSettings.FIELD_TITLE],
                artist=request.data[apiSettings.FIELD_ARTIST],
                album=request.data[apiSettings.FIELD_ALBUM],
                genre=request.data[apiSettings.FIELD_GENRE],
                rating=request.data[apiSettings.FIELD_RATING],
                language=request.data[apiSettings.FIELD_LANGUAGE],)
            
            songDBUpdatedSerializer = SongDBSerializer(songDBUpdated, context={'request': request})
            return JsonResponse(songDBUpdatedSerializer.data)

        except SongDB.DoesNotExist as exception:
            return django.views.defaults.page_not_found(request=request, exception=exception)
    
    if request.method == 'DELETE':
        LibrarySongDAO.delete(songDB)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
 
@api_view(['GET'])
def external_song_list(request):

    externalSource = request.GET.get(apiSettings.FIELD_SOURCE, False)
    query = request.GET.get(apiSettings.FIELD_QUERY, False)
    pageNumber = request.GET.get(apiSettings.FIELD_PAGE, 0)

    if externalSource == apiSettings.EXTERNAL_SOURCE_MYFREEMP3:
        externalSongs = ExternalSongMyfreemp3DAO.get_list(query, pageNumber)
        return get_json_response_paginated(request, externalSongs)

    else:
        return JsonResponse(
            {
                apiSettings.FIELD_STATUS :'false',
                apiSettings.FIELD_DURATION : apiSettings.EXTERNAL_SOURCE_DOESNT_EXIST_MESSAGE
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
 
@api_view(['POST'])
def external_song_download(request):
    externalSongUrl = request.POST[apiSettings.FIELD_EXTERNAL_SONG_URL]
    title = request.POST[apiSettings.FIELD_TITLE]
    artist = request.POST[apiSettings.FIELD_ARTIST]
    duration = request.POST[apiSettings.FIELD_DURATION]
    date = request.POST[apiSettings.FIELD_DATE]
    externalSong = ExternalSong(
        title=title, 
        artist=artist, 
        duration=duration, 
        date=date, 
        url=externalSongUrl)
    songDB = externalSongDownloadController.downloadExternalSong(request.user, externalSong)
    songDBSerializer = SongDBSerializer(songDB, data=request.data, context={'request': request})
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