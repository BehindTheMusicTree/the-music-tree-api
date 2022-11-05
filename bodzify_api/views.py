from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
import rest_framework.exceptions as exceptions

from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator

import django.views.defaults

from .serializers import UserSerializer, GroupSerializer, LibraryTrackSerializer, GenreSerializer

import bodzify_api.api.settings as apiSettings

from bodzify_api.dao.MineTrackMyfreemp3DAO import MineTrackMyfreemp3DAO
from bodzify_api.dao.UserDAO import UserDAO
from bodzify_api.dao.GenreDAO import GenreDAO

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['POST'])
def library_genre_create(request, username):
    genreCreated = GenreDAO.create(
        user=request.user, 
        genreName=request.data[apiSettings.LIBRARY_GENRE_NAME_FIELD],
        parentUuid=request.data[apiSettings.LIBRARY_GENRE_PARENT_UUID_FIELD])
    if genreCreated != None:
        return JsonResponse(GenreSerializer(genreCreated).data)
    else:
        return getHttpResponseWhenIssueWithBadRequest(request)

@api_view(['GET'])
def library_genre_list(request, username):
    if username == request.user.username:
        genres = GenreDAO.getAllByUser(request.user)
        genresData = list(GenreSerializer(genres, many=True).data)      
        return get_json_response_paginated(request, genresData)

def getHttpResponseWhenPermissionDenied(request):
    return django.views.defaults.permission_denied(
                request=request, 
                exception=exceptions.PermissionDenied)

def getHttpResponseWhenIssueWithBadRequest(request):
    return django.views.defaults.bad_request(
                request=request, 
                exception=exceptions.bad_request)
    
@api_view(['GET'])
def mine_track_list(request):
    mineSource = request.GET.get(apiSettings.MINE_FIELD_SOURCE, False)
    query = request.GET.get(apiSettings.FIELD_QUERY, False)
    pageNumber = request.GET.get(apiSettings.FIELD_PAGE, 0)

    if mineSource == apiSettings.MINE_SOURCE_MYFREEMP3:
        mineTracks = MineTrackMyfreemp3DAO.get_list(query, pageNumber)
        return get_json_response_paginated(request, mineTracks)

    else:
        return JsonResponse(
            {
                apiSettings.FIELD_STATUS :'false',
                apiSettings.FIELD_DURATION : apiSettings.MINE_SOURCE_DOESNT_EXIST_MESSAGE
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
 
@api_view(['POST'])
def mine_track_download(request):
    libraryTrack = MineTrackMyfreemp3DAO.download(
        user=request.user, 
        title=request.data[apiSettings.FIELD_TITLE], 
        artist=request.data[apiSettings.FIELD_ARTIST], 
        duration=request.data[apiSettings.FIELD_DURATION], 
        releaseDate=request.data[apiSettings.FIELD_RELEASE_DATE], 
        mineTrackUrl=request.data[apiSettings.MINE_FIELD_SONG_URL])

    return JsonResponse(LibraryTrackSerializer(libraryTrack).data)
    
@api_view(['POST'])
def user_create(request):
    username=request.data[apiSettings.USER_FIELD_USERNAME]
    if UserDAO.exists(username=username) == True:
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)

    user = UserDAO.create(
        username=username,
        email=request.data[apiSettings.USER_FIELD_EMAIL], 
        password=request.data[apiSettings.USER_FIELD_PASSWORD])
    return JsonResponse(UserSerializer(user).data)

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