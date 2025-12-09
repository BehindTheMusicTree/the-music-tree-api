
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import APIException

from api.model.all_tracks_mixin.AllTracksMixin import AllTracksMixin
from api.model.user.User import User
from api.serializer.model.track.output.minimum import TrackMinimumSerializer
from api.serializer.SerializerType import SerializerType
from api.view.viewset.model.AppModelViewSet import AppModelViewSet


class AllTracksViewSet(AppModelViewSet[AllTracksMixin]):
    def __init__(self, **kwargs):
        super().__init__(model_class=AllTracksMixin,
                         simple_serializer_class=TrackMinimumSerializer,
                         **kwargs)

    def get_object(self):
        user = self.request.user
        if not isinstance(user, User):
            raise ValueError('User is not instance of User')
        return user.all_tracks_mixin

    @extend_schema(responses=TrackMinimumSerializer(many=True))
    def list(self, args, **kwargs):
        # Validate filters
        dummy_qs = self.get_queryset()
        self.filter_queryset(dummy_qs)

        allTracksMixin = self.get_object()
        page = self.paginate_queryset(allTracksMixin.tracks_not_archived_sorted)

        if page is not None:
            serializer = self._require_serializer(SerializerType.SIMPLE)(page, many=True)
            data = list(serializer.data)
        else:
            data = []

        return self.get_paginated_response(data)
