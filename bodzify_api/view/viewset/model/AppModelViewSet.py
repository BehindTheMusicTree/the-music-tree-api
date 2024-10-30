#!/usr/bin/env python

import re

from django.db import IntegrityError
from django.http import QueryDict
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, ListSerializer
from rest_framework.exceptions import APIException
from rest_framework import viewsets
from typing import Union, Any, Type, Optional

from bodzify_api.model.base.utils.public_standard_resource.PublicStandardResource import Fields as ModelFields
from bodzify_api.model.base.utils.base_model.BaseModel import BaseModel
from bodzify_api.service.Service import Service
from bodzify_api.view import utility


class PaginatedResponseFields:
    OVERALL_TOTAL = 'overallTotal'
    NEXT = 'next'
    PREVIOUS = 'previous'
    RESULTS = 'results'


class AppModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(
            self,
            service: Optional[Service],
            model_class: type[BaseModel],
            filter_class: Optional[Any] = None,
            detailed_serializer_class: Optional[Type[ModelSerializer]] = None,
            **kwargs):
        super().__init__(**kwargs)
        self.service = service
        self.model_class = model_class
        self.filter_class = filter_class
        self.detailed_serializer_class = detailed_serializer_class

    @staticmethod
    def camel_to_snake(name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @staticmethod
    def get_dict_with_snake_case_keys_from_form_data(form_data):
        snake_case_dict = {}
        if isinstance(form_data, QueryDict):
            for key, values in form_data.lists():
                snake_case_key = AppModelViewSet.camel_to_snake(key)
                if len(values) > 1:
                    snake_case_dict[snake_case_key] = values
                else:
                    snake_case_dict[snake_case_key] = values[0]
        elif isinstance(form_data, dict):
            for key, value in form_data.items():
                snake_case_key = AppModelViewSet.camel_to_snake(key)
                snake_case_dict[snake_case_key] = value
        return snake_case_dict

    @staticmethod
    def get_dict_in_snake_case_keys_from_dict_in_camel_case_keys(dict_in_camel_case_keys):
        snake_case_dict = {}
        for key, value in dict_in_camel_case_keys.items():
            snake_case_key = AppModelViewSet.camel_to_snake(key)
            snake_case_dict[snake_case_key] = value
        return snake_case_dict

    def _get_detailed_serializer_class(self) -> Type[ModelSerializer]:
        if not self.detailed_serializer_class:
            raise NotImplementedError(
                'You must define detailed_serializer_class in your viewset initialization'
            )
        return self.detailed_serializer_class

    def _get_detailed_serializer_instance(self, instance) -> Union[ListSerializer, ModelSerializer, Any]:
        serializer_class = self._get_detailed_serializer_class()
        if serializer_class is not None:
            return serializer_class(instance=instance)
        raise ValidationError("Serializer class not defined")

    def _create(self, request, *args, **kwargs):
        if not self.service:
            raise NotImplementedError("Service not defined in viewset")

        request_data_snake_case = self.get_dict_with_snake_case_keys_from_form_data(request.data)
        try:
            instance = self.service.create(post_data=request_data_snake_case, request=request)
            response_serializer = self._get_detailed_serializer_instance(instance=instance)
            headers = self.get_success_headers(response_serializer.data)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except (IntegrityError, ValidationError) as exception:
            return utility.get_response_when_bad_request(exception=exception)

    def _update(self, request, *args, **kwargs):
        if not self.service:
            raise NotImplementedError("Service not defined in viewset")

        request_data_snake_case = self.get_dict_with_snake_case_keys_from_form_data(request.data)
        updatedinstance = self.service.update(put_data=request_data_snake_case,
                                              oldinstance=self.get_object(),
                                              request=request)
        response_serializer = self._get_detailed_serializer_instance(updatedinstance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK, headers=headers)

    def get_queryset(self):
        try:
            snake_case_params = self.get_dict_in_snake_case_keys_from_dict_in_camel_case_keys(self.request.GET)
            queryset = self.model_class.objects.filter(user=self.request.user)

            if self.filter_class:
                queryset = self.filter_class(snake_case_params, queryset=queryset).qs

            ordering_fields = self.model_class.objects.get_default_ordering()
            return queryset.order_by(*ordering_fields)
        except ValidationError as e:
            raise ValidationError(e.detail)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            page = self.paginate_queryset(queryset)
            if page:
                data = self._get_detailed_serializer_class()(page, many=True).data

            if not queryset.exists():
                data = []

            return self.get_paginated_response(data)
        except ValidationError as e:
            return Response(
                {"detail": str(e.detail[0])},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _destroy(self, request, *args, **kwargs):
        if not self.service:
            raise NotImplementedError("Service not defined in viewset")

        self.service.delete(user=request.user, instance=self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_paginated_response(self, data):
        if not self.paginator:
            raise APIException("Pagination not set", code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if data:
            return Response({
                PaginatedResponseFields.OVERALL_TOTAL: self.paginator.page.paginator.count,
                PaginatedResponseFields.NEXT: self.paginator.get_next_link(),
                PaginatedResponseFields.PREVIOUS: self.paginator.get_previous_link(),
                PaginatedResponseFields.RESULTS: data
            })
        else:
            return Response({
                PaginatedResponseFields.OVERALL_TOTAL: 0,
                PaginatedResponseFields.NEXT: None,
                PaginatedResponseFields.PREVIOUS: None,
                PaginatedResponseFields.RESULTS: []
            })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self._get_detailed_serializer_instance(instance)
        return Response(serializer.data)
