from django.db import transaction
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema  # type: ignore

from bodzify_api.filter.set.CriteriaFilterSet import CriteriaFilterSet, Fields as FilterFields
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.criteria.input.schema.endpoint.post import CriteriaPostSerializer
from bodzify_api.serializer.schema.criteria.input.schema.endpoint.put import CriteriaPutSerializer
from bodzify_api.serializer.schema.criteria.input.schema.schema import CriteriaSchemaSerializer
from bodzify_api.serializer.schema.criteria.output.detailed import CriteriaDetailedSerializer
from bodzify_api.serializer.schema.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class CriteriaViewSet(AppModelViewSet[Criteria]):
    def __init__(self, **kwargs):
        super().__init__(
            model_class=Criteria,
            filter_class=CriteriaFilterSet,
            simple_serializer_class=CriteriaSimpleSerializer,
            detailed_serializer_class=CriteriaDetailedSerializer,
            create_serializer_class=CriteriaPostSerializer,
            update_serializer_class=CriteriaPutSerializer,
            **kwargs
        )

    @transaction.atomic
    @extend_schema(request=CriteriaSchemaSerializer, responses=CriteriaDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._post(request, *args, **kwargs)

    @extend_schema(parameters=[OpenApiParameter(name=FilterFields.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=FilterFields.PARENT,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY,
                                                required=False)],
                   responses=CriteriaSimpleSerializer)
    def list(self, request, *args, **kwargs):
        return self._list(request, *args, **kwargs)

    @transaction.atomic
    @extend_schema(request=CriteriaSchemaSerializer,
                   responses=CriteriaDetailedSerializer,
                   description=("""Updates a criteria"""))
    def update(self, request, *args, **kwargs):
        return self._update(request, *args, **kwargs)
