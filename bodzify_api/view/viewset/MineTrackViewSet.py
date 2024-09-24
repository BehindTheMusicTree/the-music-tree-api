#!/usr/bin/env python

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from bodzify_api.serializer.mine.track.detailed import MineTrackSerializer
from bodzify_api.serializer.track.input.endpoint.extract import LibTrackExtractSerializer
from bodzify_api.service.mine import MineService
import bodzify_api.view.utility as utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


class GetFields:
    SOURCE = "source"
    QUERY = "query"


class MineTrackViewSet(MultiSerializerViewSet):

    serializers = {
        'list':  MineTrackSerializer,
        'extract':  LibTrackExtractSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, MineTrackSerializer)

    @extend_schema(parameters=[
        OpenApiParameter(GetFields.SOURCE, OpenApiTypes.STR, OpenApiParameter.PATH),
        OpenApiParameter(GetFields.QUERY, OpenApiTypes.STR, OpenApiParameter.PATH),
        OpenApiParameter(utility.REQUEST_PAGINATED_PAGE_FIELD, OpenApiTypes.INT, OpenApiParameter.PATH)])
    def list(self, request):
        mine_source = request.GET.get(GetFields.SOURCE, False)
        query = request.GET.get(GetFields.QUERY, False)
        page_number = request.GET.get(utility.REQUEST_PAGINATED_PAGE_FIELD, 0)

        mine_tracks = MineService.List(baseurl=mine_source, query=query, page_number=page_number)
        response_serializer = MineTrackSerializer(mine_tracks, many=True)
        headers = self.get_success_headers(response_serializer.data)

        return utility.get_json_response_paginated(request=request,
                                                   data_json_list=response_serializer.data,
                                                   headers=headers)
