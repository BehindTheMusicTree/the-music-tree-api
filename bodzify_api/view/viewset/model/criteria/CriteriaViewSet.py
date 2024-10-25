#!/usr/bin/env python

from django.db import transaction
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework.serializers import ModelSerializer

from bodzify_api.model.criteria.Criteria import Fields, Criteria
from bodzify_api.serializer.schema.criteria.input.schema.schema import CriteriaSchemaSerializer
from bodzify_api.serializer.schema.criteria.output.detailed import CriteriaDetailedSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class FilterFields:
    NAME = Fields.NAME
    PARENT = Fields.PARENT


class CriteriaViewSet(AppModelViewSet):

    queryset = Criteria.objects.all()
    serializers = {
        'default': CriteriaDetailedSerializer,
        'list':  CriteriaDetailedSerializer,
        'retrieve':  CriteriaDetailedSerializer,
        'create':  CriteriaSchemaSerializer,
        'update':  CriteriaSchemaSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        name = self.request.query_params.get(FilterFields.NAME)  # type: ignore
        if name:
            queryset = queryset.filter(name__contains=name)

        parentParameter = self.request.query_params.get(FilterFields.PARENT)  # type: ignore
        if parentParameter:
            if parentParameter == "":
                parent = None
            else:
                parent = parentParameter
            queryset = queryset.filter(parent=parent)

        return queryset.order_by(Fields.NAME)

    def _get_detailed_serializer(self, instance) -> ModelSerializer:
        return CriteriaDetailedSerializer(instance=instance)  # type: ignore

    @transaction.atomic
    @extend_schema(request=CriteriaSchemaSerializer, responses=CriteriaDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @extend_schema(parameters=[OpenApiParameter(name=FilterFields.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=FilterFields.PARENT,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY,
                                                required=False)],
                   responses=CriteriaDetailedSerializer)
    def list(self, request, *args, **kwargs):
        return self._list(request, *args, **kwargs)

    @transaction.atomic
    @extend_schema(request=CriteriaSchemaSerializer,
                   responses=CriteriaDetailedSerializer,
                   description=("""Updates a criteria"""))
    def update(self, request, *args, **kwargs):
        return self._update(request, *args, **kwargs)
