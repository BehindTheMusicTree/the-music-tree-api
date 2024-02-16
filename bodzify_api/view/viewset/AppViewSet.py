#!/usr/bin/env python

from abc import abstractmethod
import logging
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from bodzify_api.service.Service import Service
from bodzify_api.view import utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger('bodyzify_api')

class AppViewSet(MultiSerializerViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, service, **kwargs):
        super().__init__(**kwargs)
        self.service = service

    def _create(self, request, *args, **kwargs):
        try:
            instance = self.service.create(user=request.user, post_schema_data=request.data)
        except IntegrityError as e:
            logger.exception(e)
            return utility.get_json_response_when_bad_request(exception=e)

        response_serializer = self._get_detailed_serializer(instance=instance)
        headers = self.get_success_headers(response_serializer.data)

        return JsonResponse(data=response_serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers,
                            safe=False)
    
    def _update(self, request, *args, **kwargs):
        updated_instance = self.service.update(
            user=request.user, 
            put_schema_data=request.data, 
            old_instance=self.get_object())
        response_serializer_data = self._get_detailed_serializer(updated_instance).data
        headers = self.get_success_headers(response_serializer_data)
        return JsonResponse(
            data=response_serializer_data,
            status=status.HTTP_200_OK,
            headers=headers)
    
    def _list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)
    
    @abstractmethod
    def _get_detailed_serializer(self, instance) -> ModelSerializer:
        raise NotImplementedError("This method must be implemented in the subclass")

    @abstractmethod
    def _get_service(self) -> Service:
        raise NotImplementedError("This method must be implemented in the subclass")
    
