#!/usr/bin/env python

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from bodzify_api.serializer.mine.track.MineTrackSerializer import MineTrackSerializer
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackExtractSerializer import LibTrackExtractSerializer
from bodzify_api.service.mine import MineService
import bodzify_api.view.utility as utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


class GET_PARAMETER_NAME:
    SOURCE = "source"
    QUERY = "query"


class MineTrackViewSet(MultiSerializerViewSet):

    serializers = {
        'list':  MineTrackSerializer,
        'extract':  LibTrackExtractSerializer,
    }

    @extend_schema(parameters=[
        OpenApiParameter(GET_PARAMETER_NAME.SOURCE,
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

        mine_tracks = MineService.List(baseurl=mine_source, query=query, page_number=page_number)
        response_serializer = MineTrackSerializer(mine_tracks, many=True)
        headers = self.get_success_headers(response_serializer.data)

        return utility.get_json_response_paginated(
            request=request,
            data_json_list=response_serializer.data,
            headers=headers)
