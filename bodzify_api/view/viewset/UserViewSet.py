#!/usr/bin/env python

from rest_framework.decorators import action
from rest_framework import status, viewsets

from django.contrib.auth.models import User
from django.http import JsonResponse

from bodzify_api.serializer.UserSerializer import UserSerializer
from rest_framework.permissions import IsAdminUser


USER_USERNAME_FIELD = 'username'
USER_PASSWORD_FIELD = 'password'
USER_EMAIL_FIELD = 'email'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        requestSerializer = UserSerializer(data=request.data)
        requestSerializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=request.data[USER_USERNAME_FIELD],
            password=request.data[USER_PASSWORD_FIELD],
            email=request.data[USER_EMAIL_FIELD])
        responseSerializer = UserSerializer(user)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(responseSerializer.data, status=status.HTTP_201_CREATED, headers=headers)