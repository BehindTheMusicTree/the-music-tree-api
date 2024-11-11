from bodzify_api.model.user.User import User
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request

from bodzify_api.serializer.schema.user.detailed import UserDetailedSerializer
from bodzify_api.view.viewset.base.AppModelViewSet import AppModelViewSet


class UserViewSet(AppModelViewSet[User]):
    serializer_class = UserDetailedSerializer
    permission_classes = [IsAdminUser]

    def __init__(self, **kwargs):
        super().__init__(model_class=User, detailed_serializer_class=UserDetailedSerializer, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        return self._handle_post(request, *args, **kwargs)
