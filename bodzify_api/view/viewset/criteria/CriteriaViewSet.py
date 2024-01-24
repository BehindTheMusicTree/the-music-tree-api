#!/usr/bin/env python

from django.db import IntegrityError
from django.http import JsonResponse, QueryDict
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.view import utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.serializer.criteria.input.CriteriaPostSchemaSerializer import CriteriaPostSchemaSerializer
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import CriteriaDetailedSerializer
from bodzify_api.service.criteria.CriteriaService import CriteriaService
from bodzify_api.model.criteria.Criteria import Criteria, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL


class FILTER_FIELDS:
    NAME = CRITERIA_ATTRIBUTES_LABEL.NAME
    PARENT = CRITERIA_ATTRIBUTES_LABEL.PARENT


class CriteriaViewSet(MultiSerializerViewSet):

    queryset = Criteria.objects.all()
    serializers = {
        'default': CriteriaDetailedSerializer,
        'list':  CriteriaDetailedSerializer,
        'retrieve':  CriteriaDetailedSerializer,
        'create':  CriteriaPostSchemaSerializer,
    }

    def __init__(self, criteriaService: CriteriaService, **kwargs):
        super().__init__(**kwargs)
        self.criteriaService = criteriaService

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        name = self.request.query_params.get(FILTER_FIELDS.NAME)
        if name is not None:
            queryset = queryset.filter(name__contains=name)

        parentParameter = self.request.query_params.get(FILTER_FIELDS.PARENT)
        if parentParameter is not None:
            if parentParameter == "":
                parent = None
            else:
                parent = parentParameter
            queryset = queryset.filter(parent=parent)

        return queryset

    @extend_schema(request=CriteriaPostSchemaSerializer,
                   responses=CriteriaDetailedSerializer)
    def create(self, request, *args, **kwargs):
        try:
            criteria = self.criteriaService.create(user=request.user, data=request.data)
        except IntegrityError as e:
            return utility.get_json_response_when_bad_request(exception=e)

        responseSerializer = CriteriaDetailedSerializer(criteria)
        headers = self.get_success_headers(responseSerializer.data)

        return JsonResponse(data=responseSerializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers,
                            safe=False)

    @extend_schema(parameters=[OpenApiParameter(name=FILTER_FIELDS.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=FILTER_FIELDS.PARENT,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY,
                                                required=False)],
                   responses=CriteriaDetailedSerializer)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
