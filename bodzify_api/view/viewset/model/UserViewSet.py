#!/usr/bin/env python

from bodzify_api.model.user.User import User
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from bodzify_api.serializer.schema.user.detailed import UserSerializer


class Fields:
    USERNAME = 'username'
    PASSWORD = 'password'
    EMAIL = 'email'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        requestSerializer = UserSerializer(data=request.data)
        requestSerializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=request.data[Fields.USERNAME],
            password=request.data[Fields.PASSWORD],
            email=request.data[Fields.EMAIL])
        response_serializer = UserSerializer(user)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
