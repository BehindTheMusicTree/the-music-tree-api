from drf_spectacular.types import OpenApiTypes  # type: ignore
from drf_spectacular.utils import OpenApiParameter, extend_schema  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore

from bodzify_api.filtering.set.criteria.Fields import Fields as FilterFields
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.model.criteria.input.post import CriteriaPostSerializer
from bodzify_api.serializer.model.criteria.input.put import CriteriaPutSerializer
from bodzify_api.serializer.model.criteria.output.detailed import CriteriaDetailedSerializer
from bodzify_api.serializer.model.criteria.output.simple import CriteriaSimpleSerializer

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

    @extend_schema(request=CriteriaPostSerializer, responses=CriteriaDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._handle_post(request)

    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    def destroy(self, request, *args, **kwargs):
        """
        Delete a criteria.

        When deleting a criteria:
        - If it has children and a parent, children are reassigned to the parent
        - If it has children but no parent, children become root criteria
        - If it's a root criteria, tracks are moved to the criterialess playlist
        - The criteria playlist is deleted along with the criteria
        """
        return self._handle_destroy()

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

    @extend_schema(request=CriteriaPutSerializer,
                   responses=CriteriaDetailedSerializer,
                   description="""Updates a criteria""")
    def update(self, request, *args, **kwargs):
        return self._handle_update(request)
