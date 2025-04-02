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
            # Create a children field with no max_nodes_count param to skip node counting for children
            from bodzify_api.serializer.field.TreeField import TreeField
            # Use keyword arguments to exclude max_nodes_count entirely
            kwargs = {
                'allow_empty': True,
            }
            self._children_field = TreeField(**kwargs)
            # Ensure the children field has the same child serializer
            self._children_field.child = self.child
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
        print(f"TREE FIELD - Starting validation with data type: {type(data)}")
        if isinstance(data, list) and len(data) > 0:
            print(f"TREE FIELD - First node: {data[0]}")
            if isinstance(data[0], dict) and 'children' in data[0]:
                print(f"TREE FIELD - First node's children: {data[0]['children']}")
                if isinstance(data[0]['children'], list) and len(data[0]['children']) > 0:
                    print(f"TREE FIELD - First node's first child: {data[0]['children'][0]}")

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

        # Create a deep copy of the data to preserve child structure
        import copy
        data_copy = copy.deepcopy(data)

        # Validate each node with CriteriaTreeNodeSerializer
        validated_data = []
        for i, node in enumerate(data):
            node_children = None

            # Store the original children before validation
            if isinstance(node, dict) and Fields.CHILDREN in node:
                print(f"TREE FIELD - Node {i} has children before validation: {node[Fields.CHILDREN]}")
                node_children = copy.deepcopy(node[Fields.CHILDREN])

            # Check for missing or empty name fields directly before passing to serializer
            if isinstance(node, dict):
                from bodzify_api.serializer.model.criteria.input.Fields import Fields as InputFields

                # Handle missing name
                if InputFields.NAME_PUBLIC not in node:
                    raise AppValidationException(
                        field_name=self.field_name,  # Use serializer field name for public-facing errors
                        message="Invalid tree structure: each node must have a name",
                        field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID
                    )

                # Handle empty name (special case with specific field name and error code)
                if InputFields.NAME_PUBLIC in node and node[InputFields.NAME_PUBLIC] == "":
                    raise AppValidationException(
                        field_name=InputFields.NAME_PUBLIC,  # Use 'name' field for empty name errors
                        message="The field cannot be empty",
                        field_validation_error_code=FieldValidationErrorCode.NAME_EMPTY
                    )

            try:
                validated_node = self.child.run_validation(node)
                if validated_node is None:
                    # Use the serializer field name for validation errors
                    raise AppValidationException(
                        field_name=self.field_name,
                        message="Invalid tree structure: each node must have a name",
                        field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID
                    )

                print(f"TREE FIELD - Node {i} validated with keys: {validated_node.keys()}")

                # Ensure children field exists with original data
                if node_children is not None:
                    print(f"TREE FIELD - Restoring original children for node {i}")
                    validated_node[Fields.CHILDREN] = node_children
                elif Fields.CHILDREN not in validated_node:
                    validated_node[Fields.CHILDREN] = []

                # Handle None children
                if validated_node[Fields.CHILDREN] is None:
                    validated_node[Fields.CHILDREN] = []

                validated_data.append(validated_node)
            except Exception as e:
                # Only propagate validation errors for specific cases
                if isinstance(e, AppValidationException):
                    # Let specific AppValidationException pass through
                    raise
                else:
                    # Wrap other exceptions with appropriate field name
                    raise AppValidationException(
                        field_name=self.field_name,
                        message=str(e),
                        field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID
                    )

        # Process children recursively
        for i, node in enumerate(validated_data):
            # Process non-empty children recursively
            if Fields.CHILDREN in node and node[Fields.CHILDREN]:
                print(f"TREE FIELD - Processing children for node {i}: {node[Fields.CHILDREN]}")
                node[Fields.CHILDREN] = self.children_field.run_validation(node[Fields.CHILDREN])
                print(f"TREE FIELD - Children after validation: {node[Fields.CHILDREN]}")

        print(f"TREE FIELD - Returning {len(validated_data)} validated nodes")
        if validated_data and len(validated_data) > 0:
            print(f"TREE FIELD - First validated node: {validated_data[0]}")
            if Fields.CHILDREN in validated_data[0]:
                print(f"TREE FIELD - First node children after validation: {validated_data[0][Fields.CHILDREN]}")

        return validated_data

    def _check_for_duplicate_names(self, data: list) -> None:
        if not data or not isinstance(data, list):
            return

        from bodzify_api.serializer.model.criteria.input.Fields import Fields as InputFields
        names = []

        for node in data:
            if isinstance(node, dict) and InputFields.NAME_PUBLIC in node:
                name = node[InputFields.NAME_PUBLIC]
                if name in names:
                    raise AppValidationException(
                        field_name=self.field_name,  # Use serializer field name
                        message="Tree contains duplicate values",
                        field_validation_error_code=FieldValidationErrorCode.TREE_VALUE_DUPLICATE
                    )
                names.append(name)
