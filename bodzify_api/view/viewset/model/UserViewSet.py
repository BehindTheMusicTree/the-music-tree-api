from typing import Any

from django.db import transaction
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from bodzify_api.model.user.User import User
from bodzify_api.serializer.model.user.output.detailed import UserDetailedSerializer
from bodzify_api.view.viewset.model.base.AppModelViewSet import AppModelViewSet


class UserViewSet(AppModelViewSet[User]):
    serializer_class = UserDetailedSerializer
    permission_classes = [IsAdminUser]

    def __init__(self, **kwargs):
        super().__init__(model_class=User,
                         simple_serializer_class=UserDetailedSerializer,
                         detailed_serializer_class=UserDetailedSerializer,
                         is_private_resource=False,
                         **kwargs)

    def list(self, *args: Any, **kwargs: Any) -> Response:
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    @transaction.atomic
    def destroy(self, *args, **kwargs):
        return self._handle_destroy()
