from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # type: ignore
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from bodzify_api.filter.set.ArtistFilterSet import ArtistFilterSet, Fields as FilterFields
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.service.ArtistService import ArtistService
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.serializer.schema.artist.detailed import ArtistDetailedSerializer


class ArtistViewSet(AppModelViewSet):
    def __init__(self, **kwargs):
        super().__init__(
            service=ArtistService(),
            model_class=Artist,
            filter_class=ArtistFilterSet,
            detailed_serializer_class=ArtistDetailedSerializer,
            **kwargs
        )

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, request, *args, **kwargs):
        return super()._list(request, *args, **kwargs)
