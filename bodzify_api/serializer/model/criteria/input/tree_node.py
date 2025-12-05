from rest_framework.serializers import DictField

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.serializer.AppInputSerializer import AppInputSerializer
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.field.AppListField import AppListField
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields


class CriteriaTreeNodeSerializer(AppInputSerializer):
    name = AppCharField(max_length=settings.CRITERIA_NAME_LEN_MAX, allow_blank=False, required=True)
    children = AppListField(child=DictField(), required=False, default=list, allow_null=True)

    def __init__(self, structure_field_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.structure_field_name = structure_field_name

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise AppValidationException(
                field_name=self.structure_field_name,
                message="Invalid tree structure: each node must be a dictionary",
                field_validation_error_code=FieldValidationErrorCode.TREE_MALFORMED
            )
        return super().to_internal_value(data)

    def validate_children(self, value):
        # Handle None values by converting to empty list
        if value is None:
            return []

        if not isinstance(value, list):
            raise ValueError(f"{Fields.CHILDREN} must be an array")

        # Handle empty list case
        if not value:
            return []

        from bodzify_api.serializer.model.criteria.input.tree_node import CriteriaTreeNodeSerializer
        validated_children = []

        for child in value:

            # Create a serializer for this child node
            serializer = CriteriaTreeNodeSerializer(structure_field_name=self.structure_field_name,
                                                    data=child)
            serializer.is_valid(raise_exception=True)

            # Get validated data for this child
            validated_child = serializer.validated_data

            # Make sure children field exists and is preserved
            if Fields.CHILDREN not in validated_child:
                validated_child[Fields.CHILDREN] = []
            elif validated_child[Fields.CHILDREN] is None:
                validated_child[Fields.CHILDREN] = []

            validated_children.append(validated_child)

        return validated_children
