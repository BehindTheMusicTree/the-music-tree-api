from drf_spectacular.utils import OpenApiParameter  # type: ignore
from drf_spectacular.types import OpenApiTypes  # type: ignore
from drf_spectacular.utils import extend_schema

from api.filtering.set.album.AlbumFilterSet import AlbumFilterSet
from api.filtering.set.album.Fields import Fields as FilterFields
from api.model.album.Album import Album
from api.serializer.model.album.detailed import AlbumDetailedSerializer
from api.serializer.model.album.simple import AlbumSimpleSerializer
from api.view.viewset.model.AppModelViewSet import AppModelViewSet


class AlbumViewSet(AppModelViewSet[Album]):
    def __init__(self, **kwargs):
        super().__init__(model_class=Album,
                         filterset_class=AlbumFilterSet,
                         simple_serializer_class=AlbumSimpleSerializer,
                         detailed_serializer_class=AlbumDetailedSerializer,
                         **kwargs)

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME_PUBLIC, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ALBUM_ARTIST_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    def destroy(self, *args, **kwargs):
        return self._handle_destroy()
