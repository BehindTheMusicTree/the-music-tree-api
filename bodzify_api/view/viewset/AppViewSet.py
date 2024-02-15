#!/usr/bin/env python

import logging
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from bodzify_api.service.Service import Service
from bodzify_api.view import utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet

logger = logging.getLogger('bodyzify_api')

class AppViewSet(MultiSerializerViewSet):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = self._get_service()

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
    
    def _get_detailed_serializer(self, instance):
        raise NotImplementedError("This method must be implemented in the subclass")
    
    def _get_service(self):
        raise NotImplementedError("This method must be implemented in the subclass")
    
