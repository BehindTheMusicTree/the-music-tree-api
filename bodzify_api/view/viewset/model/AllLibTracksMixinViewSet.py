from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError as DrfValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

from bodzify_api.model.all_lib_tracks_mixin.AllLibTracksMixin import AllLibTracksMixin
from bodzify_api.model.user.User import User
from bodzify_api.serializer.SerializerType import SerializerType
from bodzify_api.serializer.schema.model.all_lib_tracks_mixin.detailed import AllLibTracksMixinDetailedSerializer
from bodzify_api.view.error.ErrorResponse import ErrorResponse
from .base.AppModelViewSet import AppModelViewSet


class AllLibTracksViewSet(AppModelViewSet[AllLibTracksMixin]):
    def __init__(self, **kwargs):
        super().__init__(model_class=AllLibTracksMixin,
                         simple_serializer_class=AllLibTracksMixinDetailedSerializer,
                         **kwargs)

    def get_object(self):
        user = self.request.user
        if not isinstance(user, User):
            raise ValueError('User is not instance of User')
        return user.all_lib_tracks_mixin

    @extend_schema(responses=AllLibTracksMixinDetailedSerializer)
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if not queryset.exists():
                data = []
            elif page is not None:
                serializer = self._require_serializer(SerializerType.SIMPLE)(page, many=True)
                data = list(serializer.data)
            else:
                data = []

            return self.get_paginated_response(data)
        except (DrfValidationError, DjangoValidationError) as e:
            return ErrorResponse.from_validation_error(e)
