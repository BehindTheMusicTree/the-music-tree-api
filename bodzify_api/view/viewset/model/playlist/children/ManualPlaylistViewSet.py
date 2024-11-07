
from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from bodzify_api.filter.set.ManualPlaylistFilterSet import Fields, ManualPlaylistFilterSet
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.schema.playlist.children.simple.input.endpoint import ManualPlaylistInputEndpointSerializer
from bodzify_api.serializer.schema.playlist.children.simple.output.detailed import ManualPlaylistDetailedSerializer
from bodzify_api.serializer.schema.playlist.children.simple.output.simple import ManualPlaylistSimpleSerializer
from bodzify_api.service.playlist.ManualPlaylistService import ManualPlaylistService
from bodzify_api.view.viewset.base.AppModelViewSet import AppModelViewSet


class ManualPlaylistViewSet(AppModelViewSet[ManualPlaylist]):

    def __init__(self, **kwargs):
        super().__init__(
            service=ManualPlaylistService(),
            model_class=ManualPlaylist,
            filter_class=ManualPlaylistFilterSet,
            simple_serializer_class=ManualPlaylistSimpleSerializer,
            detailed_serializer_class=ManualPlaylistDetailedSerializer,
            create_serializer_class=ManualPlaylistInputEndpointSerializer,
            update_serializer_class=ManualPlaylistInputEndpointSerializer,
            ** kwargs
        )

    def get_queryset(self):
        return ManualPlaylist.objects.filter(user=self.request.user).order_by(Fields.NAME)

    @extend_schema(parameters=[
        OpenApiParameter(name=Fields.NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, request, *args, **kwargs):
        return super()._handle_list(request, *args, **kwargs)

    @transaction.atomic
    @extend_schema(request=ManualPlaylistInputEndpointSerializer, responses=ManualPlaylistDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._handle_post(request, *args, **kwargs)

    @transaction.atomic
    @extend_schema(request=ManualPlaylistInputEndpointSerializer, responses=ManualPlaylistDetailedSerializer)
    def update(self, request, *args, **kwargs):
        return self._handle_update(request, *args, **kwargs)
