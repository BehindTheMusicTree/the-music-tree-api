#!/usr/bin/env python

import logging
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.serializer.criteria.input.schema.CriteriaPostSchemaSerializer import CriteriaPostSchemaSerializer
from bodzify_api.serializer.criteria.input.schema.CriteriaUpdateSchemaSerializer import CriteriaPutSchemaSerializer
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import CriteriaDetailedSerializer

from bodzify_api.view.viewset.AppModelViewSet import AppModelViewSet
from rest_framework.serializers import ModelSerializer
from bodzify_api.model.criteria.Criteria import Criteria, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL

logger = logging.getLogger('bodzify_api')


class FILTER_FIELDS:
    NAME = CRITERIA_ATTRIBUTES_LABEL.NAME
    PARENT = CRITERIA_ATTRIBUTES_LABEL.PARENT


class CriteriaViewSet(AppModelViewSet):

    queryset = Criteria.objects.all()
    serializers = {
        'default': CriteriaDetailedSerializer,
        'list':  CriteriaDetailedSerializer,
        'retrieve':  CriteriaDetailedSerializer,
        'create':  CriteriaPostSchemaSerializer,
    }

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
    
    def _get_detailed_serializer(self, instance) -> ModelSerializer:
        return CriteriaDetailedSerializer(instance=instance) # type: ignore

    @extend_schema(request=CriteriaPostSchemaSerializer,
                   responses=CriteriaDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @extend_schema(parameters=[OpenApiParameter(name=FILTER_FIELDS.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=FILTER_FIELDS.PARENT,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY,
                                                required=False)],
                   responses=CriteriaDetailedSerializer)
    def list(self, request, *args, **kwargs):
        return self._list(request, *args, **kwargs)
    
    @extend_schema(request=CriteriaPutSchemaSerializer,
                   responses=CriteriaDetailedSerializer,
                   description=("""Updates a criteria"""))
    def update(self, request, *args, **kwargs):
        return self._update(request, *args, **kwargs)
