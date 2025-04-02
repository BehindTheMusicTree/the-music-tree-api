from typing import Any, cast

from bodzify_api import settings
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.field.AppListField import AppListField
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields
from bodzify_api.serializer.model.criteria.input.tree_node import CriteriaTreeNodeSerializer


class TreeField(AppListField):
    def __init__(self,
                 allow_empty: bool = False,
                 max_nodes_count: int = settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT,
                 **kwargs):
        # Set these before calling parent initializer
        self._children_field = None
        self.max_nodes = max_nodes_count
        self._allow_empty = allow_empty
        self._max_nodes_count = max_nodes_count

        # Initialize with a basic serializer as a temporary child
        from rest_framework import serializers
        init_child = serializers.DictField()

        # Call parent initializer
        AppListField.__init__(self, child=init_child, allow_empty=allow_empty, **kwargs)

        # Now that field_name is set by parent initializer, set the real child
        self.child = CriteriaTreeNodeSerializer(structure_field_name=cast(str, self.field_name))

    @property
    def children_field(self) -> 'TreeField':
        if self._children_field is None:
            self._children_field = TreeField(allow_empty=True)
        return self._children_field

    def _count_descendants(self, children: list) -> int:
        count = 0
        for child in children:
            if not isinstance(child, dict):
                raise AppValidationException(
                    field_name=self.get_error_field_name(),
                    message="Invalid tree structure: each node must be a dictionary",
                    field_validation_error_code=FieldValidationErrorCode.TREE_MALFORMED
                )

            # First count all descendants
            if Fields.CHILDREN in child:
                children_list = child[Fields.CHILDREN]
                if not isinstance(children_list, list):
                    print(f"Invalid children type: {type(children_list)}")
                    raise AppValidationException(
                        field_name=self.get_error_field_name(),
                        message=f"Invalid tree structure: {Fields.CHILDREN} must be an array, null, or not provided",
                        field_validation_error_code=FieldValidationErrorCode.TREE_MALFORMED
                    )
                if children_list:  # Only count if there are children
                    count += self._count_descendants(children_list)

            # Then count this node
            count += 1
        return count

    def get_error_field_name(self) -> str:
        # Use parent implementation by default
        return super().get_error_field_name()

    def run_validation(self, data: Any = None) -> Any:
        if data is None:
            if not self.allow_null:
                self.fail('null')
            return None

        if not data:
            if not self._allow_empty:
                self.fail('required')
            return []

        if not isinstance(data, list):
            raise AppValidationException(
                field_name=self.get_error_field_name(),
                message="Invalid tree structure: root must be an array",
                field_validation_error_code=FieldValidationErrorCode.TREE_MALFORMED
            )

        # Count total nodes for max_nodes validation
        total_count = 0
        for node in data:
            if not isinstance(node, dict):
                raise AppValidationException(
                    field_name=self.get_error_field_name(),
                    message="Invalid tree structure: each node must be a dictionary",
                    field_validation_error_code=FieldValidationErrorCode.TREE_MALFORMED
                )
            if self._max_nodes_count is not None:
                total_count += self._count_descendants([node])
        if self._max_nodes_count is not None and total_count > self._max_nodes_count:
            raise AppValidationException(
                field_name=self.get_error_field_name(),
                message=(f"Total number of elements ({total_count}) exceeds maximum allowed "
                         f"({self.max_nodes})"),
                field_validation_error_code=FieldValidationErrorCode.TREE_TOO_LARGE
            )

        # Check for duplicate values before detailed validation
        self._check_for_duplicate_names(data)

        # Validate each node with CriteriaTreeNodeSerializer
        validated_data = []
        for node in data:
            # Check for missing or empty name fields directly before passing to serializer
            if isinstance(node, dict):
                # Handle missing name
                if Fields.NAME_PUBLIC not in node:
                    raise AppValidationException(
                        field_name=Fields.TREE,
                        message="Invalid tree structure: each node must have a name",
                        field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID
                    )

                # Handle empty name (special case with specific field name and error code)
                if Fields.NAME_PUBLIC in node and node[Fields.NAME_PUBLIC] == "":
                    raise AppValidationException(
                        field_name=Fields.NAME_PUBLIC,  # Use 'name' field for empty name errors
                        message="The field cannot be empty",
                        field_validation_error_code=FieldValidationErrorCode.NAME_EMPTY
                    )

            try:
                validated_node = self.child.run_validation(node)
                if validated_node is None:
                    # Use the tree public field for validation errors
                    raise AppValidationException(
                        field_name=Fields.TREE,
                        message=f'Invalid tree structure: each node must have a {Fields.NAME_PUBLIC}',
                        field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID
                    )
                validated_data.append(validated_node)
            except Exception as e:
                # Let errors from the child serializer pass through as-is
                # This ensures empty name validation has the correct field name
                if not isinstance(e, AppValidationException):
                    # Only wrap non-AppValidationException errors
                    raise AppValidationException(
                        field_name=self.get_error_field_name(),
                        message=str(e),
                        field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID
                    )
                raise

        # Process children recursively
        for node in validated_data:
            children = node.get(Fields.CHILDREN)
            if children:
                node[Fields.CHILDREN] = self.children_field.run_validation(children)

        return validated_data

    def _check_for_duplicate_names(self, data: list) -> None:
        if not data or not isinstance(data, list):
            return

        names = []
        for node in data:
            if isinstance(node, dict) and Fields.NAME_PUBLIC in node:
                name = node[Fields.NAME_PUBLIC]
                if name in names:
                    raise AppValidationException(
                        field_name=Fields.TREE,
                        message="Tree contains duplicate values",
                        field_validation_error_code=FieldValidationErrorCode.TREE_VALUE_DUPLICATE
                    )
                names.append(name)
