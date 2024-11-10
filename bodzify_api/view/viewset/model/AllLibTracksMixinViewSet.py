from drf_spectacular.utils import extend_schema

from bodzify_api.model.all_lib_tracks_mixin.AllLibTracksMixin import AllLibTracksMixin
from bodzify_api.serializer.schema.lib_track_mixin.detailed import LibTrackMixinDetailedSerializer
from ..base.AppModelViewSet import AppModelViewSet


class AllLibTracksViewSet(AppModelViewSet[AllLibTracksMixin]):
    def __init__(self, **kwargs):
        super().__init__(model_class=AllLibTracksMixin,
                         detailed_serializer_class=LibTrackMixinDetailedSerializer,
                         **kwargs)

    @extend_schema(responses=LibTrackMixinDetailedSerializer)
    def list(self, request, *args, **kwargs):
        return self._handle_list(request, *args, **kwargs)
