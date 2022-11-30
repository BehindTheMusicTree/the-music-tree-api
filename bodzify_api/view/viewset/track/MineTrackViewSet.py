#!/usr/bin/env python

from rest_framework import viewsets
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from django.http import JsonResponse

from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackResponseSerializer
from bodzify_api.serializer.track.MineTrackSerializer import MineTrackSerializer
from bodzify_api.service import MineTrackMyfreemp3Service
import bodzify_api.view.utility as viewset_utility

SOURCE_MYFREEMP3 = "myfreemp3"
SOURCE_DOESNT_EXIST_MESSAGE = "The specified source doesn\'t exist"
SOURCE_FIELD = "source"
SONG_URL_FIELD = "url"
QUERY_FIELD = "query"

TITLE_FIELD = "title"
ARTIST_FIELD = "artist"
DURATION_FIELD = "duration"
RELEASED_ON_FIELD = "releasedOn"
TRACK_URL = "url"

class MineTrackViewSet(viewsets.GenericViewSet):  
    serializer_class = MineTrackSerializer
    
    @extend_schema(
        parameters=[
          OpenApiParameter(SOURCE_FIELD, OpenApiTypes.STR, OpenApiParameter.PATH),
          OpenApiParameter(QUERY_FIELD, OpenApiTypes.STR, OpenApiParameter.PATH),
          OpenApiParameter(
            viewset_utility.REQUEST_PAGINATED_PAGE_FIELD, 
            OpenApiTypes.INT, 
            OpenApiParameter.PATH)
        ],
    )
    def list(self, request):
        mineSource = request.GET.get(SOURCE_FIELD, False)
        query = request.GET.get(QUERY_FIELD, False)
        pageNumber = request.GET.get(viewset_utility.REQUEST_PAGINATED_PAGE_FIELD, 0)
        pageSize = request.GET.get(viewset_utility.REQUEST_PAGINATED_PAGE_SIZE_FIELD, 0)

        if mineSource == SOURCE_MYFREEMP3:
            mineTracks = MineTrackMyfreemp3Service.list(query, pageNumber, pageSize)
            return viewset_utility.GetJsonResponsePaginated(request, mineTracks)

        else:
            return viewset_utility.GetJsonResponseWhenBadRequest(request)
    
    @action(detail=False, methods=['post'])
    def extract(self, request):
        libraryTrack = MineTrackMyfreemp3Service.extract(
            user=request.user, 
            title=request.data[TITLE_FIELD], 
            artist=request.data[ARTIST_FIELD], 
            duration=request.data[DURATION_FIELD], 
            releasedOn=request.data[RELEASED_ON_FIELD], 
            mineTrackUrl=request.data[TRACK_URL])

        return JsonResponse(LibraryTrackResponseSerializer(libraryTrack).data)