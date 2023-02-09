#!/usr/bin/env python

from rest_framework import status
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.http import JsonResponse

from bodzify_api.serializer.track.TrackDetailedSerializer import TrackDetailedSerializer
from bodzify_api.serializer.track.MineTrackSerializer import MineTrackSerializer
from bodzify_api.service import MineTrackMyfreemp3Service
import bodzify_api.view.utility as utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


GET_SOURCE_PARAMETER_NAME = "source"
GET_SOURCE_PARAMETER_VALUE_MYFREEMP3 = "myfreemp3"
GET_SOURCE_PARAMETER_VALUE_ERROR_MESSAGE_DOESNT_EXIST = "The specified source doesn\'t exist"
GET_QUERY_PARAMETER_NAME = "query"

POST_TRACK_URL_PARAMETER_NAME = "url"
POST_TITLE_PARAMETER_NAME = "title"
POST_ARTIST_PARAMETER_NAME = "artist"
POST_DURATION_PARAMETER_NAME = "duration"
POST_RELEASED_ON_PARAMETER_NAME = "releasedOn"


class MineTrackViewSet(MultiSerializerViewSet):
    serializer_class = MineTrackSerializer

    @extend_schema(
        parameters=[
          OpenApiParameter(GET_SOURCE_PARAMETER_NAME, OpenApiTypes.STR, OpenApiParameter.PATH),
          OpenApiParameter(GET_QUERY_PARAMETER_NAME, OpenApiTypes.STR, OpenApiParameter.PATH),
          OpenApiParameter(
            utility.REQUEST_PAGINATED_PAGE_FIELD,
            OpenApiTypes.INT,
            OpenApiParameter.PATH)
        ],
    )
    def list(self, request):
        mineSource = request.GET.get(GET_SOURCE_PARAMETER_NAME, False)
        query = request.GET.get(GET_QUERY_PARAMETER_NAME, False)
        pageNumber = request.GET.get(utility.REQUEST_PAGINATED_PAGE_FIELD, 0)
        pageSize = request.GET.get(utility.REQUEST_PAGINATED_PAGE_SIZE_FIELD, 0)

        if mineSource == GET_SOURCE_PARAMETER_VALUE_MYFREEMP3:
            mineTracks = MineTrackMyfreemp3Service.List(query, pageNumber, pageSize)
            return utility.GetJsonResponsePaginated(request, mineTracks)

        else:
            return utility.GetJsonResponseWhenBadRequest(request)

    @action(detail=False, methods=['post'])
    def extract(self, request):
        libraryTrack = MineTrackMyfreemp3Service.Extract(
                user=request.user,
                title=request.data[POST_TITLE_PARAMETER_NAME],
                artist=request.data[POST_ARTIST_PARAMETER_NAME],
                duration=request.data[POST_DURATION_PARAMETER_NAME],
                releasedOn=request.data[POST_RELEASED_ON_PARAMETER_NAME],
                mineTrackUrl=request.data[POST_TRACK_URL_PARAMETER_NAME])

        responseSerializer = TrackDetailedSerializer(libraryTrack)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
            data=responseSerializer.data, status=status.HTTP_201_CREATED, headers=headers)
