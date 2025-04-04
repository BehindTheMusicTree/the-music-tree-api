
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import APIException

from bodzify_api.model.all_uploaded_tracks_mixin.AllUploadedTracksMixin import AllUploadedTracksMixin
from bodzify_api.model.user.User import User
from bodzify_api.serializer.model.uploaded_track.output.minimum import UploadedTrackMinimumSerializer
from bodzify_api.serializer.SerializerType import SerializerType
from bodzify_api.view.viewset.model.base.AppModelViewSet import AppModelViewSet


class AllUploadedTracksViewSet(AppModelViewSet[AllUploadedTracksMixin]):
    def __init__(self, **kwargs):
        super().__init__(model_class=AllUploadedTracksMixin,
                         simple_serializer_class=UploadedTrackMinimumSerializer,
                         **kwargs)

    def get_object(self):
        user = self.request.user
        if not isinstance(user, User):
            raise ValueError('User is not instance of User')
        return user.all_uploaded_tracks_mixin

    @extend_schema(responses=UploadedTrackMinimumSerializer(many=True))
    def list(self, args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        allUploadedTracksMixin: AllUploadedTracksMixin | None = queryset.first()
        if not allUploadedTracksMixin:
            raise APIException('System initialization error: User data is corrupted')
        page = self.paginate_queryset(allUploadedTracksMixin.uploaded_tracks_not_archived_sorted)

        if page is not None:
            serializer = self._require_serializer(SerializerType.SIMPLE)(page, many=True)
            data = list(serializer.data)
        else:
            data = []

        return self.get_paginated_response(data)
