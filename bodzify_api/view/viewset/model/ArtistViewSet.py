from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # type: ignore
from django.db import transaction

from bodzify_api.filter.set.ArtistFilterSet import ArtistFilterSet, Fields as FilterFields
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.view.viewset.base.AppModelViewSet import AppModelViewSet
from bodzify_api.serializer.schema.artist.detailed import ArtistDetailedSerializer


class ArtistViewSet(AppModelViewSet[Artist]):
    def __init__(self, **kwargs):
        super().__init__(
            model_class=Artist,
            filter_class=ArtistFilterSet,
            simple_serializer_class=ArtistDetailedSerializer,
            detailed_serializer_class=ArtistDetailedSerializer,
            **kwargs
        )

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, request, *args, **kwargs):
        return super()._handle_list(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete_with_albums_and_tracks()
        return Response(status=status.HTTP_204_NO_CONTENT)
