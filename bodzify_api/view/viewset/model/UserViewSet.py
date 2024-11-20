from typing import Any

from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from django.db import transaction

from bodzify_api.model.user.User import User
from bodzify_api.serializer.schema.model.user.output.detailed import UserDetailedSerializer
from bodzify_api.view.viewset.base.AppModelViewSet import AppModelViewSet


class UserViewSet(AppModelViewSet[User]):
    serializer_class = UserDetailedSerializer
    permission_classes = [IsAdminUser]

    def __init__(self, **kwargs):
        super().__init__(model_class=User, detailed_serializer_class=UserDetailedSerializer, **kwargs)

    # @transaction.atomic not needed
    def create(self, request: Request, *args, **kwargs):
        return self._handle_post(request, *args, **kwargs)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self._handle_list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return self._handle_retrieve(request, *args, **kwargs)

    # @transaction.atomic not needed
    def update(self, request, *args, **kwargs):
        return self._handle_update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return self._handle_destroy(request, *args, **kwargs)
