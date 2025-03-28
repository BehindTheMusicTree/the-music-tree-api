from typing import Type, cast, Any

from drf_spectacular.types import OpenApiTypes  # type: ignore
from drf_spectacular.utils import OpenApiParameter, extend_schema  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import action  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.serializers import Serializer

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
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

    def get_serializer_class_for_non_standard_action(self) -> Type[Serializer]:
        if self.action == 'import_tree':
            return CriteriaSimpleSerializer
        raise NotImplementedError(f"Action {self.action} not defined in viewset")

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

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        Returns a tree structure of all criteria.
        The structure follows the format:
        {
          "name": "Criteria name",
          "children": [
            {
              "name": "Child criteria name",
              "children": []
            }
          ]
        }
        """
        queryset = self.get_queryset()
        manager = cast(Any, queryset)
        tree = manager.build_criteria_tree(request.user)
        return Response(tree, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='tree/import')
    def import_tree(self, request):
        """
        Imports a tree structure of criteria, replacing all existing criteria of the current type.
        Returns a paginated list of created criteria.
        The input should be an array of criteria trees, where each tree follows the format:
        {
          "name": "Criteria name",
          "children": [
            {
              "name": "Child criteria name",
              "children": []
            }
          ]
        }
        """
        if not isinstance(request.data, list):
            raise AppValidationException(field_name="data",
                                         message="Input must be an array of criteria trees",
                                         field_validation_error_code=FieldValidationErrorCode.REQUIRED)

        if not request.data:
            raise AppValidationException(
                field_name="data",
                message="At least one criteria must be provided",
                field_validation_error_code=FieldValidationErrorCode.REQUIRED
            )

        try:
            queryset = self.get_queryset()
            manager = cast(Any, queryset)
            manager.import_criteria_tree(request.user, request.data)
        except ValueError as e:
            raise AppValidationException(
                field_name="data",
                message=str(e),
                field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID
            )

        # Get all created criteria
        queryset = self.get_queryset()
        serializer_class = cast(Type[Serializer], self.simple_serializer_class)
        serializer = serializer_class(instance=queryset, many=True)
        return self._get_post_created_response(serializer)
