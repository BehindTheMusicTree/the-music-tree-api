from queue import Empty
from typing import Any, Dict

from django.http import QueryDict
from bodzify_api.model.user.User import User, Fields as ModelFields
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.request import Request

from bodzify_api.serializer.schema.user.detailed import UserDetailedSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserDetailedSerializer
    permission_classes = [IsAdminUser]

    def __init__(self, **kwargs):
        super().__init__(
            model_class=User,
            detailed_serializer_class=UserDetailedSerializer,
            **kwargs
        )

    def create(self, request: Request, *args, **kwargs):
        requestSerializer = UserDetailedSerializer(data=request.data)
        requestSerializer.is_valid(raise_exception=True)

        if request.data is Empty:
            request_data: Dict[str, Any] = {}
        elif isinstance(request.data, dict):
            request_data: Dict[str, Any] = request.data
        elif isinstance(request.data, QueryDict):
            request_data: Dict[str, Any] = request.data.dict()
        else:
            request_data: Dict[str, Any] = {}

        user = User.objects.create_user(
            username=request_data[ModelFields.USERNAME],
            password=request_data[ModelFields.PASSWORD],
            email=request_data[ModelFields.EMAIL])
        response_serializer = UserDetailedSerializer(user)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
