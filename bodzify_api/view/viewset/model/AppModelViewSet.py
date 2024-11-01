import re
from typing import Type, Optional

from django.db import IntegrityError
from django.http import QueryDict
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import APIException
from rest_framework import viewsets

from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.model.base.utils.base_model.BaseModel import BaseModel
from bodzify_api.service.Service import Service
from bodzify_api.view import utils


class PaginatedResponseFields:
    OVERALL_TOTAL = 'overallTotal'
    NEXT = 'next'
    PREVIOUS = 'previous'
    RESULTS = 'results'


class AppModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_class: Optional[Type[AppFilterSet]] = None
    simple_serializer_class: Optional[Type[ModelSerializer]] = None
    detailed_serializer_class: Optional[Type[ModelSerializer]] = None
    create_serializer_class: Optional[Type[Serializer]] = None
    update_serializer_class: Optional[Type[Serializer]] = None

    def __init__(
            self,
            model_class: type[BaseModel],
            service: Optional[Service] = None,
            filter_class: Optional[Type[AppFilterSet]] = None,
            simple_serializer_class: Optional[Type[ModelSerializer]] = None,
            detailed_serializer_class: Optional[Type[ModelSerializer]] = None,
            update_serializer_class: Optional[Type[Serializer]] = None,
            create_serializer_class: Optional[Type[Serializer]] = None,
            **kwargs):
        super().__init__(**kwargs)
        self.model_class = model_class
        self.service = service
        self.filter_class = filter_class
        self.simple_serializer_class = simple_serializer_class
        self.detailed_serializer_class = detailed_serializer_class
        self.update_serializer_class = update_serializer_class
        self.create_serializer_class = create_serializer_class

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

    def _get_create_serializer_class_eventually_depending_on_action(self):
        if self.create_serializer_class:
            return self.create_serializer_class
        raise NotImplementedError("create_serializer_class not defined in viewset")

    def _post_depending_on_action(self, request, create_data_validated):
        print(f"[DEBUG] Action: {self.action}")
        if self.action == 'create':
            if not self.service:
                raise NotImplementedError("Service not defined in viewset")
            return self.service.post(request=request, create_data_validated=create_data_validated)
        raise NotImplementedError(f"No action defined for action {self.action}")

    def _validate_input_request_data(self, request_data):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

    def _post(self, request: Request, *args, **kwargs):
        if not self.service:
            raise NotImplementedError("Service not defined in viewset")

        create_data_snake_case = self.get_dict_with_snake_case_keys_from_form_data(request.data)
        try:
            self._validate_input_request_data(create_data_snake_case)
            instance = self._post_depending_on_action(request, create_data_snake_case)
            if not self.detailed_serializer_class:
                raise NotImplementedError("detailed_serializer_class not defined in viewset")
            response_serializer = self.detailed_serializer_class(instance=instance)
            headers = self.get_success_headers(response_serializer.data)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except (IntegrityError, RestValidationError) as exception:
            return utils.get_response_when_bad_request(exception=exception)

    def _update(self, request, *args, **kwargs):
        if not self.service:
            raise NotImplementedError("Service not defined in viewset")

        request_data_snake_case = self.get_dict_with_snake_case_keys_from_form_data(request.data)
        try:
            self._validate_input_request_data(request_data_snake_case)
            self.service.update(put_data=request_data_snake_case, oldinstance=self.get_object(), request=request)
            if not self.detailed_serializer_class:
                raise NotImplementedError("detailed_serializer_class not defined in viewset")
            response_serializer = self.detailed_serializer_class(instance=instance)
            headers = self.get_success_headers(response_serializer.data)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK, headers=headers)
        except (IntegrityError, RestValidationError) as exception:
            return utils.get_response_when_bad_request(exception=exception)

    def _list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            page = self.paginate_queryset(queryset)
            if page:
                if not self.simple_serializer_class:
                    raise NotImplementedError("simple_serializer_class not defined in viewset")
                data = self.simple_serializer_class(page, many=True).data

            if not queryset.exists():
                data = []

            return self.get_paginated_response(data)
        except RestValidationError as e:
            return Response(data={"detail": str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        request: Request = self.request  # type: ignore
        try:
            snake_case_params = self.get_dict_in_snake_case_keys_from_dict_in_camel_case_keys(request.query_params)
            queryset = self.model_class.objects.filter(user=request.user)

            if self.filter_class:
                queryset = self.filter_class(snake_case_params, queryset=queryset).qs

            ordering_fields = self.model_class.objects.get_default_ordering()
            return queryset.order_by(*ordering_fields)
        except DjangoValidationError as e:
            raise RestValidationError(e)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == 'retrieve':
            if not self.detailed_serializer_class:
                raise NotImplementedError('You must define detailed_serializer_class in your viewset initialization')
            return self.detailed_serializer_class
        elif self.action == 'create':
            return self._get_create_serializer_class_eventually_depending_on_action()
        elif self.action == 'update' or self.action == 'partial_update':
            if not self.update_serializer_class:
                raise NotImplementedError('You must define update_serializer_class in your viewset initialization')
            return self.update_serializer_class
        raise NotImplementedError("action not defined in viewset")

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
        serializer = self.detailed_serializer_class(instance)
        return Response(serializer.data)
