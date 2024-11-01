from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # type: ignore
from rest_framework.response import Response
from rest_framework import status

from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.filter.set.AlbumFilterSet import AlbumFilterSet, Fields as FilterFields
from bodzify_api.model.album.Album import Album
from bodzify_api.serializer.schema.album.simple import AlbumSimpleSerializer
from bodzify_api.serializer.schema.album.detailed import AlbumDetailedSerializer


class AlbumViewSet(AppModelViewSet[Album]):
    def __init__(self, **kwargs):
        super().__init__(
            model_class=Album,
            filter_class=AlbumFilterSet,
            simple_serializer_class=AlbumSimpleSerializer,
            detailed_serializer_class=AlbumDetailedSerializer,
            **kwargs
        )

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ALBUM_ARTISTS_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, request, *args, **kwargs):
        return super()._handle_list(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete_with_tracks_and_eventually_artists()
        return Response(status=status.HTTP_204_NO_CONTENT)
