#!/usr/bin/env python

from rest_framework.decorators import action
from rest_framework import status

from drf_spectacular.utils import extend_schema

from django.http import JsonResponse

from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackSerializer
from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackResponseSerializer
from bodzify_api.model.track.LibraryTrack import LibraryTrack
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

    def get_queryset(self):
        queryset = LibraryTrack.objects.all()
        genreParameter = self.request.query_params.get(GENRE_FIELD)
        if genreParameter == "": genre = None
        else: genre = genreParameter
        return queryset.filter(genre=genre)

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
            track=LibraryTrackDao.get(uuid=pk))
        