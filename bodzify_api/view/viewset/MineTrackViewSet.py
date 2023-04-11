#!/usr/bin/env python
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.serializer.track.output.MineTrackSerializer import MineTrackSerializer
from bodzify_api.serializer.track.input.schema.TrackExtractSchemaSerializer import TrackExtractSchemaSerializer
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
        'extract':  TrackExtractSchemaSerializer,
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
