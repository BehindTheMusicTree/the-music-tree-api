#!/usr/bin/env python
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from django.http import JsonResponse
from bodzify_api.serializer.UserSerializer import UserSerializer
from rest_framework.permissions import IsAdminUser

USERNAME_PARAMETER_NAME = 'username'
PASSWORD_PARAMETER_NAME = 'password'
EMAIL_PARAMETER_NAME = 'email'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        requestSerializer = UserSerializer(data=request.data)
        requestSerializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=request.data[USERNAME_PARAMETER_NAME],
            password=request.data[PASSWORD_PARAMETER_NAME],
            email=request.data[EMAIL_PARAMETER_NAME])
        responseSerializer = UserSerializer(user)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
            responseSerializer.data, status=status.HTTP_201_CREATED, headers=headers)
