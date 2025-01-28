from django.db import transaction
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema  # type: ignore
from rest_framework.response import Response  # type: ignore

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.filtering.set.criteria.Fields import Fields as FilterFields
from bodzify_api.serializer.schema.model.criteria.input.post import CriteriaPostSerializer
from bodzify_api.serializer.schema.model.criteria.input.put import CriteriaPutSerializer
from bodzify_api.serializer.schema.model.criteria.output.detailed import CriteriaDetailedSerializer
from bodzify_api.serializer.schema.model.criteria.output.simple import CriteriaSimpleSerializer
from ..base.AppModelViewSet import AppModelViewSet


class CriteriaViewSet(AppModelViewSet[Criteria]):
    def __init__(self, model_class: type[Criteria], **kwargs):
        # Filtersets must be imported after Django is loaded
        from bodzify_api.filtering.set.criteria.CriteriaFilterSet import CriteriaFilterSet
        super().__init__(model_class=model_class,
                         filterset_class=CriteriaFilterSet,
                         simple_serializer_class=CriteriaSimpleSerializer,
                         detailed_serializer_class=CriteriaDetailedSerializer,
                         create_serializer_class=CriteriaPostSerializer,
                         update_serializer_class=CriteriaPutSerializer,
                         **kwargs)

    @transaction.atomic
    @extend_schema(request=CriteriaPostSerializer, responses=CriteriaDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._handle_post(request)

    @extend_schema(parameters=[OpenApiParameter(name=FilterFields.NAME_PUBLIC,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=FilterFields.PARENT,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY,
                                                required=False)],
                   responses=CriteriaSimpleSerializer)
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs) -> Response:
        return self._handle_retrieve()

    @ transaction.atomic
    @ extend_schema(request=CriteriaPutSerializer,
                    responses=CriteriaDetailedSerializer,
                    description="""Updates a criteria""")
    def update(self, request, *args, **kwargs):
        return self._handle_update(request)
