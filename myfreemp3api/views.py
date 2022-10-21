from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
import django.views.defaults

from .serializers import UserSerializer, GroupSerializer, LibrarySongSerializer

import myfreemp3api.api.settings as apiSettings
from myfreemp3api.models import LibrarySong

from myfreemp3api.dao.librarySongDAO import LibrarySongDAO
from myfreemp3api.dao.mineSongMyfreemp3DAO import MineSongMyfreemp3DAO

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['GET'])
def library_song_list(request, userId):
    try:
        lirarySongs = LibrarySong.objects.filter(user=request.user)
        librarySongsData = list(LibrarySongSerializer(lirarySongs, many=True).data)        
        return get_json_response_paginated(request, librarySongsData)

    except LibrarySong.DoesNotExist as exception:
        return django.views.defaults.page_not_found(request=request, exception=exception)

@api_view(['GET', 'PUT', 'DELETE'])
def library_song_detail(request, userId, songId):

    if request.method == 'GET':
        try:
            return JsonResponse(LibrarySongSerializer(LibrarySongDAO.get(uuid=songId)).data)
        except LibrarySong.DoesNotExist as exception:
            return django.views.defaults.page_not_found(request=request, exception=exception)

    if request.method == 'PUT':        
        try:
            songDBUpdated = LibrarySongDAO.update(
                uuid=songId,
                title=request.data[apiSettings.FIELD_TITLE],
                artist=request.data[apiSettings.FIELD_ARTIST],
                album=request.data[apiSettings.FIELD_ALBUM],
                genre=request.data[apiSettings.FIELD_GENRE],
                rating=request.data[apiSettings.FIELD_RATING],
                language=request.data[apiSettings.FIELD_LANGUAGE],)
            
            return JsonResponse(LibrarySongSerializer(songDBUpdated).data)

        except LibrarySong.DoesNotExist as exception:
            return django.views.defaults.page_not_found(request=request, exception=exception)
    
    if request.method == 'DELETE':
        LibrarySongDAO.delete(uuid=songId)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
 
@api_view(['GET'])
def mine_song_list(request):

    mineSource = request.GET.get(apiSettings.MINE_FIELD_SOURCE, False)
    query = request.GET.get(apiSettings.FIELD_QUERY, False)
    pageNumber = request.GET.get(apiSettings.FIELD_PAGE, 0)

    if mineSource == apiSettings.MINE_SOURCE_MYFREEMP3:
        mineSongs = MineSongMyfreemp3DAO.get_list(query, pageNumber)
        return get_json_response_paginated(request, mineSongs)

    else:
        return JsonResponse(
            {
                apiSettings.FIELD_STATUS :'false',
                apiSettings.FIELD_DURATION : apiSettings.MINE_SOURCE_DOESNT_EXIST_MESSAGE
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
 
@api_view(['POST'])
def mine_song_download(request):
    
    librarySong = MineSongMyfreemp3DAO.download(
        user=request.user, 
        title=request.POST[apiSettings.FIELD_TITLE], 
        artist=request.POST[apiSettings.FIELD_ARTIST], 
        duration=request.POST[apiSettings.FIELD_DURATION], 
        date=request.POST[apiSettings.FIELD_DATE], 
        mineSongUrl=request.POST[apiSettings.MINE_FIELD_SONG_URL])

    return JsonResponse(LibrarySongSerializer(librarySong).data)
    
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