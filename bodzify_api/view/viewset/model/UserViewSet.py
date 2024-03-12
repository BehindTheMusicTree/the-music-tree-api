#!/usr/bin/env python

from rest_framework import status, viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from bodzify_api.serializer.UserSerializer import UserSerializer
from rest_framework.permissions import IsAdminUser


class PARAMETER_NAME:
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
            username=request.data[PARAMETER_NAME.USERNAME],
            password=request.data[PARAMETER_NAME.PASSWORD],
            email=request.data[PARAMETER_NAME.EMAIL])
        response_serializer = UserSerializer(user)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
