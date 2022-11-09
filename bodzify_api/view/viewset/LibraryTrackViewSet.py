#!/usr/bin/env python

from rest_framework.decorators import action
from rest_framework import status, viewsets

from drf_spectacular.utils import extend_schema
import logging
from django.http import JsonResponse

from bodzify_api.serializer.LibraryTrackSerializer import LibraryTrackSerializer
from bodzify_api.serializer.LibraryTrackSerializer import LibraryTrackResponseSerializer
from bodzify_api.models import LibraryTrack
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.dao import LibraryTrackDao
from bodzify_api.view import utility

TITLE_FIELD = "title"
ARTIST_FIELD = "artist"
ALBUM_FIELD = "album"
GENRE_FIELD = "genre"
RATING_FIELD = "rating"
LANGUAGE_FIELD = "language"
DURATION_FIELD = "duration"
RELEASE_DATE_FIELD = "releasedOn"

class LibraryTrackViewSet(MultiSerializerViewSet):
    queryset = LibraryTrack.objects.all()
    serializers = {
        'default': LibraryTrackSerializer,
        'list':  LibraryTrackResponseSerializer,
        'retrieve':  LibraryTrackResponseSerializer,
    }

    @extend_schema(
        request=LibraryTrackSerializer,
        responses=LibraryTrackResponseSerializer
    )
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        track = LibraryTrack.objects.get(uuid=kwargs['pk'])
        LibraryTrackDao.updateTags(track)
        serializer = LibraryTrackResponseSerializer(track)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        return utility.GetFileResponseForTrackDownload(
            request=request, 
            trackModel=LibraryTrackDao.get(uuid=pk))
        