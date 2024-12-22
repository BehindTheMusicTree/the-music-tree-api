from typing import Optional
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError as DrfValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

from bodzify_api.model.all_lib_tracks_mixin.AllLibTracksMixin import AllLibTracksMixin
from bodzify_api.model.user.User import User
from bodzify_api.serializer.SerializerType import SerializerType
from bodzify_api.serializer.schema.model.lib_track.output.minimum import LibTrackMinimumSerializer
from bodzify_api.view.error.ErrorResponse import ErrorResponse
from bodzify_api.view.viewset.model.base.AppModelViewSet import AppModelViewSet


class AllLibTracksViewSet(AppModelViewSet[AllLibTracksMixin]):
    def __init__(self, **kwargs):
        super().__init__(model_class=AllLibTracksMixin,
                         simple_serializer_class=LibTrackMinimumSerializer,
                         **kwargs)

    def get_object(self):
        user = self.request.user
        if not isinstance(user, User):
            raise ValueError('User is not instance of User')
        return user.all_lib_tracks_mixin

    @extend_schema(responses=LibTrackMinimumSerializer(many=True))
    def list(self, args, **kwargs):
        try:
            allLibTracksMixin: Optional[AllLibTracksMixin] = self.get_queryset().first()
            if not allLibTracksMixin:
                raise DrfValidationError('No AllLibTracksMixin object found for user')
            page = self.paginate_queryset(allLibTracksMixin.lib_tracks_sorted)

            if page is not None:
                serializer = self._require_serializer(SerializerType.SIMPLE)(page, many=True)
                data = list(serializer.data)
            else:
                data = []

            return self.get_paginated_response(data)
        except (DrfValidationError, DjangoValidationError) as e:
            return ErrorResponse.from_validation_error(e)
