#!/usr/bin/env python

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.serializer.track.output.MineTrackSerializer import MineTrackSerializer
from bodzify_api.serializer.track.input.schema.TrackExtractSchemaSerializer import TrackExtractSchemaSerializer
from bodzify_api.service import MineService
import bodzify_api.view.utility as utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


class GET_PARAMETER_NAME:
    SOURCE = "source"
    QUERY = "query"


GET_SOURCE_PARAMETER_VALUE_MYFREEMP3 = "myfreemp3"
GET_SOURCE_PARAMETER_VALUE_ERROR_MESSAGE_DOESNT_EXIST = "The specified source doesn\'t exist"


class MineTrackViewSet(MultiSerializerViewSet):

    serializers = {
        'list':  MineTrackSerializer,
        'extract':  TrackExtractSchemaSerializer,
    }

    @extend_schema(parameters=[OpenApiParameter(GET_PARAMETER_NAME.SOURCE,
                                                OpenApiTypes.STR,
                                                OpenApiParameter.PATH),
                               OpenApiParameter(GET_PARAMETER_NAME.QUERY,
                                                OpenApiTypes.STR,
                                                OpenApiParameter.PATH),
                               OpenApiParameter(utility.REQUEST_PAGINATED_PAGE_FIELD,
                                                OpenApiTypes.INT,
                                                OpenApiParameter.PATH)])
    def list(self, request):
        mine_source = request.GET.get(GET_PARAMETER_NAME.SOURCE, False)
        query = request.GET.get(GET_PARAMETER_NAME.QUERY, False)
        page_number = request.GET.get(utility.REQUEST_PAGINATED_PAGE_FIELD, 0)
        page_size = request.GET.get(
            utility.REQUEST_PAGINATED_PAGE_SIZE_FIELD, 0)

        if mine_source == GET_SOURCE_PARAMETER_VALUE_MYFREEMP3:
            mine_tracks = MineService.List(
                query, page_number, page_size)
            return utility.get_json_response_paginated(request, mine_tracks)

        else:
            return utility.get_json_response_when_bad_request(request)
