from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema  # type: ignore

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.model.playlist.base.output.detailed import PlaylistDetailedSerializer
from bodzify_api.serializer.model.playlist.base.output.simple import PlaylistSimpleSerializer
from bodzify_api.view.viewset.model.base.AppModelViewSet import AppModelViewSet
from bodzify_api.filtering.set.playlist.PlaylistFilterSet import PlaylistFilterSet
from bodzify_api.filtering.set.playlist.Fields import Fields as QueryParamsFields


class PlaylistViewSet(AppModelViewSet[Playlist]):

    def __init__(self, **kwargs):
        super().__init__(model_class=Playlist,
                         filterset_class=PlaylistFilterSet,
                         simple_serializer_class=PlaylistSimpleSerializer,
                         detailed_serializer_class=PlaylistDetailedSerializer,
                         **kwargs)

    @staticmethod
    def _get_queryset_str_filter_value_to_filter_nothing():
        return ''

    @extend_schema(parameters=[OpenApiParameter(name=QueryParamsFields.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=QueryParamsFields.TYPE_LABEL_INTERNAL,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()
