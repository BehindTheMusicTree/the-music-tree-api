from typing import Any

from rest_framework.fields import ListField

from bodzify_api import settings
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.field.AppDictField import AppDictField
from bodzify_api.serializer.field.AppField import AppField
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields


class TreeField(AppField, ListField):
    def __init__(self,
                 allow_empty: bool = False,
                 max_nodes_count: int = settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT,
                 **kwargs):
        ListField.__init__(self, child=AppDictField(), allow_empty=allow_empty, **kwargs)
        self.max_nodes = max_nodes_count
        self._allow_empty = allow_empty
        self._max_nodes_count = max_nodes_count
        self._children_field = None

    @property
    def children_field(self) -> 'TreeField':
        if self._children_field is None:
            self._children_field = TreeField(allow_empty=True)
        return self._children_field

    def _count_descendants(self, children: list) -> int:
        """Count total number of descendants in the tree"""
        count = 0
        for child in children:
            if not isinstance(child, dict):
                print(f"Invalid child type: {type(child)}")
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

    def run_validation(self, data: Any = None) -> Any:
        print("\n=== TreeField.run_validation ===")
        print(f"Max nodes allowed: {self.max_nodes}")

        if data is None:
            print("Data is None")
            if not self.allow_null:
                self.fail('null')
            return None

        if not data:
            print("Data is empty")
            if not self.allow_empty:
                self.fail('required')
            return []

        # First validate basic structure
        if not isinstance(data, list):
            print(f"Invalid data type: {type(data)}")
            raise AppValidationException(
                field_name=self.get_error_field_name(),
                message="Invalid tree structure: root must be an array",
                field_validation_error_code=FieldValidationErrorCode.TREE_MALFORMED
            )

        # Then validate structure and count nodes
        print("Validating tree structure and counting nodes...")
        print(f"Max allowed nodes: {self.max_nodes}")
        total_count = 0
        for node in data:
            if not isinstance(node, dict):
                print(f"Invalid node type: {type(node)}")
                raise AppValidationException(
                    field_name=self.get_error_field_name(),
                    message="Invalid tree structure: each node must be a dictionary",
                    field_validation_error_code=FieldValidationErrorCode.TREE_MALFORMED
                )
            if self._max_nodes_count is not None:
                print('Counting descendants...')
                total_count += self._count_descendants([node])
                print('calculated descendants count:', total_count)
            print(f"Running total: {total_count}")
        print(f"Total node count: {total_count}")
        if self._max_nodes_count is not None and total_count > self._max_nodes_count:
            print(f"Too many nodes: {total_count} > {self.max_nodes}")
            raise AppValidationException(
                field_name=self.get_error_field_name(),
                message=(f"Total number of elements ({total_count}) exceeds maximum allowed "
                         f"({self.max_nodes})"),
                field_validation_error_code=FieldValidationErrorCode.TREE_TOO_LARGE
            )

        # Then run ListField's validation to skip AppField's to_internal_value
        print("Running ListField validation...")
        try:
            # Call ListField's validation chain directly
            value = ListField.to_internal_value(self, data)
            ListField.run_validators(self, value)
        except Exception as e:
            print(f"ListField validation error: {e}")
            return None

        # Process children recursively
        print("Processing children recursively...")
        for node in value:
            children = node.get(Fields.CHILDREN)
            if children:
                node[Fields.CHILDREN] = self.children_field.run_validation(children)

        return value
