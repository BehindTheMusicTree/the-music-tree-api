#!/usr/bin/env python

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.serializer.mine.track.MineTrackSerializer import MineTrackSerializer
from bodzify_api.serializer.track.input.schema.TrackExtractSchemaSerializer import TrackExtractSchemaSerializer
from bodzify_api.service.mine import MineService
import bodzify_api.view.utility as utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


class GET_PARAMETER_NAME:
    SOURCE = "source"
    QUERY = "query"


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
        pageNumber = request.GET.get(utility.REQUEST_PAGINATED_PAGE_FIELD, 0)

        mineTracks = MineService.List(
            baseUrl=mineSource, query=query, pageNumber=pageNumber)
        responseSerializer = MineTrackSerializer(mineTracks, many=True)
        headers = self.get_success_headers(responseSerializer.data)

        return utility.get_json_response_paginated(
            request=request, 
            data_json_list=responseSerializer.data, 
            headers=headers)
