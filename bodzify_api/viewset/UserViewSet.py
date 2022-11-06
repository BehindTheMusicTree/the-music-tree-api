#!/usr/bin/env python

from rest_framework.decorators import action
from rest_framework import status, permissions

from django.contrib.auth.models import User
from django.http import JsonResponse

from bodzify_api.viewset.BaseViewSet import BaseViewSet
from bodzify_api.serializers import UserSerializer

class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # This logic was taken from the `create` on `ModelViewSet`. Alter as needed.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)