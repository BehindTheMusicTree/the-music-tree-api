from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from api.filtering.set.playlist.children.criteria.CriteriaPlaylistFilterSet import CriteriaPlaylistFilterSet
from api.filtering.set.playlist.children.criteria.Fields import Fields as FilterFields
from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.serializer.model.playlist.children.criteria.output.detailed import CriteriaPlaylistDetailedSerializer
from api.serializer.model.playlist.children.criteria.output.simple import CriteriaPlaylistSimpleSerializer
from api.view.viewset.model.AppModelViewSet import AppModelViewSet


class CriteriaPlaylistViewSet(AppModelViewSet[CriteriaPlaylist]):

    def __init__(self, model_class, **kwargs):
        super().__init__(service=None,
                         model_class=model_class if model_class else CriteriaPlaylist,
                         filterset_class=CriteriaPlaylistFilterSet,
                         simple_serializer_class=CriteriaPlaylistSimpleSerializer,
                         detailed_serializer_class=CriteriaPlaylistDetailedSerializer,
                         **kwargs)

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME_PUBLIC,
                         type=OpenApiTypes.STR,
                         location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.PARENT,
                         type=OpenApiTypes.STR,
                         location=OpenApiParameter.QUERY)
    ])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()
