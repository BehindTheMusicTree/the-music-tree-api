#!/usr/bin/env python

from rest_framework.decorators import action
from rest_framework import status, viewsets

from django.contrib.auth.models import User
from django.http import JsonResponse

from bodzify_api.serializer.UserSerializer import UserSerializer

USER_USERNAME_FIELD = 'username'
USER_PASSWORD_FIELD = 'password'
USER_EMAIL_FIELD = 'email'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(
            username=request.data[USER_USERNAME_FIELD],
            password=request.data[USER_PASSWORD_FIELD],
            email=request.data[USER_EMAIL_FIELD])
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)