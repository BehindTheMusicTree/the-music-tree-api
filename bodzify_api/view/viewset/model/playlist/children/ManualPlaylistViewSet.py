from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from bodzify_api.filtering.set.playlist.children.manual.ManualPlaylistFilterSet import Fields, ManualPlaylistFilterSet
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.schema.model.playlist.children.manual.input.endpoint \
    import ManualPlaylistBaseInputSerializer
from bodzify_api.serializer.schema.model.playlist.children.manual.output.detailed \
    import ManualPlaylistDetailedSerializer
from bodzify_api.serializer.schema.model.playlist.children.manual.output.simple import ManualPlaylistSimpleSerializer
from bodzify_api.view.viewset.model.base.AppModelViewSet import AppModelViewSet


class ManualPlaylistViewSet(AppModelViewSet[ManualPlaylist]):

    def __init__(self, **kwargs):
        super().__init__(model_class=ManualPlaylist,
                         filterset_class=ManualPlaylistFilterSet,
                         simple_serializer_class=ManualPlaylistSimpleSerializer,
                         detailed_serializer_class=ManualPlaylistDetailedSerializer,
                         create_serializer_class=ManualPlaylistBaseInputSerializer,
                         update_serializer_class=ManualPlaylistBaseInputSerializer,
                         **kwargs)

    def get_queryset(self):
        return ManualPlaylist.objects.filter(user=self.request.user).order_by(Fields.NAME)

    # @transaction.atomic not needed
    @extend_schema(request=ManualPlaylistBaseInputSerializer, responses=ManualPlaylistDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._handle_post(request)

    @extend_schema(parameters=[
        OpenApiParameter(name=Fields.NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    # @transaction.atomic not needed
    @extend_schema(request=ManualPlaylistBaseInputSerializer, responses=ManualPlaylistDetailedSerializer)
    def update(self, request, *args, **kwargs):
        return self._handle_update(request, *args, **kwargs)
