from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # type: ignore
from django.db import transaction

from bodzify_api.filtering.set.artist.ArtistFilterSet import ArtistFilterSet, Fields as FilterFields
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.view.viewset.model.base.AppModelViewSet import AppModelViewSet
from bodzify_api.serializer.model.artist.detailed import ArtistDetailedSerializer


class ArtistViewSet(AppModelViewSet[Artist]):
    def __init__(self, **kwargs):
        super().__init__(model_class=Artist,
                         filterset_class=ArtistFilterSet,
                         simple_serializer_class=ArtistDetailedSerializer,
                         detailed_serializer_class=ArtistDetailedSerializer,
                         **kwargs)

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME_PUBLIC, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    @transaction.atomic
    def destroy(self, *args, **kwargs):
        return self._handle_destroy()
