#!/usr/bin/env python

from django.db import transaction
from rest_framework.serializers import ModelSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from bodzify_api.serializer.criteria.input.schema.CriteriaSchemaSerializer import CriteriaSaveSchemaSerializer
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import CriteriaDetailedSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL


class FILTER_FIELDS:
    NAME = ATTRIBUTES_LABEL.NAME
    PARENT = ATTRIBUTES_LABEL.PARENT


class CriteriaViewSet(AppModelViewSet):

    queryset = Criteria.objects.all()
    serializers = {
        'default': CriteriaDetailedSerializer,
        'list':  CriteriaDetailedSerializer,
        'retrieve':  CriteriaDetailedSerializer,
        'create':  CriteriaSaveSchemaSerializer,
        'update':  CriteriaSaveSchemaSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        name = self.request.query_params.get(FILTER_FIELDS.NAME)  # type: ignore
        if name is not None:
            queryset = queryset.filter(name__contains=name)

        parentParameter = self.request.query_params.get(FILTER_FIELDS.PARENT)  # type: ignore
        if parentParameter is not None:
            if parentParameter == "":
                parent = None
            else:
                parent = parentParameter
            queryset = queryset.filter(parent=parent)

        return queryset.order_by(ATTRIBUTES_LABEL.NAME)

    def _get_detailed_serializer(self, instance) -> ModelSerializer:
        return CriteriaDetailedSerializer(instance=instance)  # type: ignore

    @transaction.atomic
    @extend_schema(request=CriteriaSaveSchemaSerializer, responses=CriteriaDetailedSerializer)
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

    @transaction.atomic
    @extend_schema(request=CriteriaSaveSchemaSerializer,
                   responses=CriteriaDetailedSerializer,
                   description=("""Updates a criteria"""))
    def update(self, request, *args, **kwargs):
        return self._update(request, *args, **kwargs)
