#!/usr/bin/env python
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.http import JsonResponse
from bodzify_api.serializer.track.output.TrackDetailedSerializer import TrackDetailedSerializer
from bodzify_api.serializer.track.output.MineTrackSerializer import MineTrackSerializer
from bodzify_api.serializer.track.input.MineTrackExtractSchemaSerializer import MineTrackExtractSchemaSerializer
from bodzify_api.service import MineTrackMyfreemp3Service
import bodzify_api.view.utility as utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


GET_SOURCE_PARAMETER_NAME = "source"
GET_SOURCE_PARAMETER_VALUE_MYFREEMP3 = "myfreemp3"
GET_SOURCE_PARAMETER_VALUE_ERROR_MESSAGE_DOESNT_EXIST = "The specified source doesn\'t exist"
GET_QUERY_PARAMETER_NAME = "query"


class MineTrackViewSet(MultiSerializerViewSet):
    
    serializers = {
        'list':  MineTrackSerializer,
        'extract':  MineTrackExtractSchemaSerializer,
    }

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


    @extend_schema(
        request=MineTrackExtractSchemaSerializer, 
        responses=TrackDetailedSerializer,
        description=("""
            Download a track from myfreemp3. 
            It is done by providing an URL and metadata:
                - "title" (required);
                - "artistName";
                - "albumName";
                - "albumArtistsName";
                - "genreName";
                - "rating";
                - "releasedOn";
                - "language";
            """)
    )
    @action(detail=False, methods=['post'])
    def extract(self, request, *args, **kwargs):
        serializer = MineTrackExtractSchemaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        libraryTrack = MineTrackMyfreemp3Service.Extract(user=request.user, requestData=request.data)
        responseSerializer = TrackDetailedSerializer(libraryTrack)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
            data=responseSerializer.data, status=status.HTTP_201_CREATED, headers=headers)
