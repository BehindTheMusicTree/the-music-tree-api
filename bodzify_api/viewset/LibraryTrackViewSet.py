#!/usr/bin/env python

from rest_framework import status
from rest_framework.decorators import action

import django.views.defaults
from django.http import JsonResponse, HttpResponse

from bodzify_api.serializers import LibraryTrackSerializer
from bodzify_api.models import LibraryTrack
from bodzify_api.dao.LibraryTrackDAO import LibraryDAO
from bodzify_api.viewset.BaseViewSet import BaseViewSet
from bodzify_api.models import Genre

TITLE_FIELD = "title"
ARTIST_FIELD = "artist"
ALBUM_FIELD = "album"
GENRE_FIELD = "genre"
RATING_FIELD = "rating"
LANGUAGE_FIELD = "language"
DURATION_FIELD = "duration"
RELEASE_DATE_FIELD = "releaseDate"

class LibraryTrackViewSet(BaseViewSet):
    serializer_class = LibraryTrackSerializer
    queryset = LibraryTrack.objects.all()

    def update(self, request, pk=None):
        genre = Genre.objects.get(uuid=request.data[GENRE_FIELD])
        try:
            trackDBUpdated = LibraryDAO.update(
                uuid=pk,
                title=request.data[TITLE_FIELD],
                artist=request.data[ARTIST_FIELD],
                album=request.data[ALBUM_FIELD],
                genre=genre,
                rating=request.data[RATING_FIELD],
                language=request.data[LANGUAGE_FIELD],)
            
            return JsonResponse(LibraryTrackSerializer(trackDBUpdated).data)

        except LibraryTrack.DoesNotExist as exception:
            return django.views.defaults.page_not_found(request=request, exception=exception)
        
    def delete(self, request, pk=None):
        LibraryDAO.delete(uuid=pk)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        return BaseViewSet.getFileResponseForTrackDownload(request=request, trackModel=LibraryDAO.get(uuid=pk))
        