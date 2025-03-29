from rest_framework.serializers import ListField, DictField

from bodzify_api import settings
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.model.criteria.input.tree_node import CriteriaTreeNodeSerializer
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields


class CriteriaTreeImportSerializer(AppSerializer):
    tree: ListField = ListField(
        child=DictField(), allow_empty=False, max_length=settings.CRITERIA_TREE_IMPORT_MAX_ROOT_COUNT)

    def to_internal_value(self, data):
        if isinstance(data, list):
            if not data:
                raise AppValidationException(field_name=Fields.TREE_INTERNAL,
                                             message="At least one criteria must be provided",
                                             field_validation_error_code=FieldValidationErrorCode.REQUIRED)
            return {Fields.TREE_INTERNAL: data}
        raise AppValidationException(field_name=Fields.TREE_INTERNAL,
                                     message="Input must be an array",
                                     field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID)

    def validate_data(self, value):
        total_count = 0
        for node in value:
            validated_node = CriteriaTreeNodeSerializer(data=node).is_valid(raise_exception=True)
            total_count += 1
            if Fields.CHILDREN in node:
                total_count += self._count_children(node[Fields.CHILDREN])

        if total_count > settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT:
            raise AppValidationException(
                field_name=Fields.TREE_INTERNAL,
                message=(f"Total number of elements ({total_count}) exceeds maximum allowed "
                         f"({settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT})"),
                field_validation_error_code=FieldValidationErrorCode.LIST_TOO_LONG
            )
        return value

    def _count_children(self, children):
        count = 0
        for child in children:
            count += 1
            if Fields.CHILDREN in child:
                count += self._count_children(child[Fields.CHILDREN])
        return count
