
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from bodzify_api.filter.set.GenrePlaylistFilterSet import GenrePlaylistFilterSet, Fields as FilterFields
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.playlist.children.criteria.output.detailed import CriteriaPlaylistDetailedSerializer
from bodzify_api.serializer.schema.playlist.children.criteria.output.simple import CriteriaPlaylistSimpleSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class GenrePlaylistViewSet(AppModelViewSet[CriteriaPlaylist]):
    def __init__(self, **kwargs):
        super().__init__(
            service=None,
            model_class=CriteriaPlaylist,
            filter_class=GenrePlaylistFilterSet,
            simple_serializer_class=CriteriaPlaylistSimpleSerializer,
            detailed_serializer_class=CriteriaPlaylistDetailedSerializer,
            **kwargs
        )

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME,
                         type=OpenApiTypes.STR,
                         location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.PARENT,
                         type=OpenApiTypes.STR,
                         location=OpenApiParameter.QUERY)
    ])
    def list(self, request, *args, **kwargs):
        return super()._handle_list(request, *args, **kwargs)
