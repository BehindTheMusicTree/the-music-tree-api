#!/usr/bin/env python

from rest_framework import viewsets
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from django.http import JsonResponse

from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackResponseSerializer
from bodzify_api.serializer.PlaylistSerializer import PlaylistSerializer
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.dao import MineTrackMyfreemp3Dao
import bodzify_api.view.utility as viewset_utility
from bodzify_api.model.playlist.Playlist import Playlist

QUERY_PARAMETER = "query"
ARTIST_FIELD = "artist"
DURATION_FIELD = "duration"
RELEASED_ON_FIELD = "releasedOn"
TRACK_URL = "url"

class PlaylistViewSet(MultiSerializerViewSet):  
    queryset = Playlist.objects.all()
    serializers = {
        'default': PlaylistSerializer,
        'list':  PlaylistSerializer,
        'retrieve':  PlaylistSerializer,
    }

    
    @extend_schema(
        parameters=[
          OpenApiParameter(QUERY_PARAMETER, OpenApiTypes.STR, OpenApiParameter.PATH)
        ]
    )
    def list(self, request):
        mineSource = request.GET.get(SOURCE_FIELD, False)
        query = request.GET.get(QUERY_FIELD, False)
        pageNumber = request.GET.get(viewset_utility.REQUEST_PAGINATED_PAGE_FIELD, 0)
        pageSize = request.GET.get(viewset_utility.REQUEST_PAGINATED_PAGE_SIZE_FIELD, 0)

        if mineSource == SOURCE_MYFREEMP3:
            mineTracks = MineTrackMyfreemp3Dao.list(query, pageNumber, pageSize)
            return viewset_utility.GetJsonResponsePaginated(request, mineTracks)

        else:
            return viewset_utility.GetJsonResponseWhenBadRequest(request)
    
    @action(detail=False, methods=['post'])
    def extract(self, request):
        libraryTrack = MineTrackMyfreemp3Dao.extract(
            user=request.user, 
            title=request.data[TITLE_FIELD], 
            artist=request.data[ARTIST_FIELD], 
            duration=request.data[DURATION_FIELD], 
            releasedOn=request.data[RELEASED_ON_FIELD], 
            mineTrackUrl=request.data[TRACK_URL])

        return JsonResponse(LibraryTrackResponseSerializer(libraryTrack).data)