from drf_spectacular.utils import OpenApiParameter  # type: ignore
from drf_spectacular.types import OpenApiTypes  # type: ignore
from drf_spectacular.utils import extend_schema

from bodzify_api.filtering.set.spotify.artist.SpotifyArtistFilterSet import SpotifyArtistFilterSet
from bodzify_api.filtering.set.spotify.artist.Fields import Fields as FilterFields
from bodzify_api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from bodzify_api.serializer.model.spotify.artist.output.detailed import SpotifyArtistDetailedSerializer
from bodzify_api.serializer.model.spotify.artist.output.simple import SpotifyArtistSimpleSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class SpotifyArtistViewSet(AppModelViewSet[SpotifyArtist]):
    def __init__(self, **kwargs):
        super().__init__(model_class=SpotifyArtist,
                         filterset_class=SpotifyArtistFilterSet,
                         detailed_serializer_class=SpotifyArtistDetailedSerializer,
                         simple_serializer_class=SpotifyArtistSimpleSerializer,
                         is_private_resource=False,
                         **kwargs)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return super().get_queryset().none()
        return super().get_queryset().distinct()

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME_PUBLIC, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.POPULARITY_MIN, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.POPULARITY_MAX, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.CREATED_ON, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.CREATED_ON_GT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.CREATED_ON_LT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.CREATED_ON_GTE, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.CREATED_ON_LTE, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.UPDATED_ON, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.UPDATED_ON_GT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.UPDATED_ON_LT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.UPDATED_ON_GTE, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.UPDATED_ON_LTE, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
    ])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()
