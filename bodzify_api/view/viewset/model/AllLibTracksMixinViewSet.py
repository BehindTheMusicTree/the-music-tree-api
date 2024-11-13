from drf_spectacular.utils import extend_schema

from bodzify_api.model.all_lib_tracks_mixin.AllLibTracksMixin import AllLibTracksMixin
from bodzify_api.model.user.User import User
from bodzify_api.serializer.schema.all_lib_tracks_mixin.detailed import AllLibTracksMixinDetailedSerializer
from ..base.AppModelViewSet import AppModelViewSet


class AllLibTracksViewSet(AppModelViewSet[AllLibTracksMixin]):
    def __init__(self, **kwargs):
        super().__init__(model_class=AllLibTracksMixin,
                         detailed_serializer_class=AllLibTracksMixinDetailedSerializer,
                         **kwargs)

    def get_object(self):
        user = self.request.user
        if not isinstance(user, User):
            raise ValueError('User is not instance of User')
        return user.all_lib_tracks_mixin

    @extend_schema(responses=AllLibTracksMixinDetailedSerializer)
    def list(self, request, *args, **kwargs):
        return self._handle_retrieve(request, *args, **kwargs)
