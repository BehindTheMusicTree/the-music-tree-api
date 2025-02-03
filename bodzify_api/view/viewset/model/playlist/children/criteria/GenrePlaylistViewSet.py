from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from bodzify_api.filtering.set.playlist.children.criteria.CriteriaPlaylistFilterSet import CriteriaPlaylistFilterSet
from bodzify_api.model.playlist.children.criteria.Fields import Fields
from bodzify_api.model.playlist.children.criteria.genre.GenrePlaylist import GenrePlaylist
from bodzify_api.serializer.schema.model.playlist.children.criteria.output.detailed import CriteriaPlaylistDetailedSerializer
from bodzify_api.serializer.schema.model.playlist.children.criteria.output.simple import CriteriaPlaylistSimpleSerializer
from bodzify_api.view.viewset.model.base.AppModelViewSet import AppModelViewSet


@extend_schema(parameters=[
    OpenApiParameter(
        name=Fields.NAME,
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description='Filter by name'
    ),
    OpenApiParameter(
        name=Fields.PARENT,
        type=OpenApiTypes.UUID,
        location=OpenApiParameter.QUERY,
        description='Filter by parent UUID'
    ),
    OpenApiParameter(
        name=Fields.ROOT,
        type=OpenApiTypes.UUID,
        location=OpenApiParameter.QUERY,
        description='Filter by root UUID'
    )
])
class GenrePlaylistViewSet(AppModelViewSet[GenrePlaylist]):
    filterset_class = CriteriaPlaylistFilterSet
    detailed_serializer_class = CriteriaPlaylistDetailedSerializer
    simple_serializer_class = CriteriaPlaylistSimpleSerializer

    def __init__(self, **kwargs):
        super().__init__(model_class=GenrePlaylist, **kwargs)
