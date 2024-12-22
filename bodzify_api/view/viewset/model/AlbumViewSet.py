from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # type: ignore
from rest_framework.response import Response
from rest_framework import status

from bodzify_api.view.viewset.model.base.AppModelViewSet import AppModelViewSet
from bodzify_api.filter.set.album.AlbumFilterSet import AlbumFilterSet
from bodzify_api.filter.set.album.Fields import Fields as FilterFields
from bodzify_api.model.album.Album import Album
from bodzify_api.serializer.schema.model.album.simple import AlbumSimpleSerializer
from bodzify_api.serializer.schema.model.album.detailed import AlbumDetailedSerializer


class AlbumViewSet(AppModelViewSet[Album]):
    def __init__(self, **kwargs):
        super().__init__(model_class=Album,
                         filterset_class=AlbumFilterSet,
                         simple_serializer_class=AlbumSimpleSerializer,
                         detailed_serializer_class=AlbumDetailedSerializer,
                         **kwargs)

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ALBUM_ARTIST_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    @transaction.atomic
    def destroy(self, *args, **kwargs):
        return self._handle_destroy()
