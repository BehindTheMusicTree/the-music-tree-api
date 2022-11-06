#!/usr/bin/env python

from rest_framework import viewsets, exceptions, status
from rest_framework.pagination import PageNumberPagination

import django.views.defaults
from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.paginator import Paginator

import bodzify_api.api.settings as apiSettings
from bodzify_api.serializers import LibraryTrackSerializer
from bodzify_api.models import LibraryTrack, Genre
from bodzify_api.dao.LibraryTrackDAO import LibraryDAO
from bodzify_api.dao.GenreDAO import GenreDAO

def getHttpResponseWhenPermissionDenied(request):
    return django.views.defaults.permission_denied(
                request=request, 
                exception=exceptions.PermissionDenied)

def getHttpResponseWhenIssueWithBadRequest(request):
    return django.views.defaults.bad_request(
                request=request, 
                exception=exceptions.bad_request)

def get_json_response_paginated(request, dataJsonList):
    pageNumber = request.GET.get(apiSettings.FIELD_PAGE, 0)
    paginator = Paginator(dataJsonList, PageNumberPagination.page_size)
    page_object = paginator.get_page(pageNumber)

    return JsonResponse({
        apiSettings.RESPONSE_PAGINATED_COUNT: len(dataJsonList),
        apiSettings.RESPONSE_PAGINATED_CURRENT: pageNumber,
        apiSettings.RESPONSE_PAGINATED_NEXT: page_object.has_next(),
        apiSettings.RESPONSE_PAGINATED_PREVIOUS: page_object.has_previous(),
        apiSettings.RESPONSE_PAGINATED_DATA: dataJsonList
    })

class LibraryTrackViewSet(viewsets.ModelViewSet):
    serializer_class = LibraryTrackSerializer
    queryset = LibraryTrack.objects.all()

    def list(self, request):
        libraryTracks = LibraryDAO.getAllByUser(request.user)
        libraryTracksData = list(LibraryTrackSerializer(libraryTracks, many=True).data)        
        return get_json_response_paginated(request, libraryTracksData)

    def retrieve(self, request, pk=None):
        try:
            return JsonResponse(LibraryTrackSerializer(LibraryDAO.get(uuid=pk)).data)
        except LibraryTrack.DoesNotExist as exception:
            return django.views.defaults.page_not_found(request=request, exception=exception)

    def update(self, request, pk=None):
        genre = GenreDAO.get(uuid=request.data[apiSettings.FIELD_GENRE])
        try:
            trackDBUpdated = LibraryDAO.update(
                uuid=pk,
                title=request.data[apiSettings.FIELD_TITLE],
                artist=request.data[apiSettings.FIELD_ARTIST],
                album=request.data[apiSettings.FIELD_ALBUM],
                genre=genre,
                rating=request.data[apiSettings.FIELD_RATING],
                language=request.data[apiSettings.FIELD_LANGUAGE],)
            
            return JsonResponse(LibraryTrackSerializer(trackDBUpdated).data)

        except LibraryTrack.DoesNotExist as exception:
            return django.views.defaults.page_not_found(request=request, exception=exception)
        
    def delete(self, request, pk=None):
        LibraryDAO.delete(uuid=pk)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    def download(request, username, trackUuid):
        track = LibraryDAO.get(uuid=trackUuid)
        fileHandle = open(track.path, "rb")

        response = FileResponse(fileHandle, content_type='whatever')
        response['Content-Length'] = os.path.getsize(track.path)
        response['Content-Disposition'] = 'attachment; filename="%s"' % track.filename

        return response