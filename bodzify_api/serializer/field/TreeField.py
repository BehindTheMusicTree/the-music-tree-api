from typing import Any

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
        AppListField.__init__(self, child=CriteriaTreeNodeSerializer(), allow_empty=allow_empty, **kwargs)
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

    def run_validation(self, data: Any = None) -> Any:
        if data is None:
            if not self.allow_null:
                self.fail('null')
            return None

        if not data:
            if not self.allow_empty:
                self.fail('required')
            return []

        if not isinstance(data, list):
            raise AppValidationException(
                field_name=self.get_error_field_name(),
                message="Invalid tree structure: root must be an array",
                field_validation_error_code=FieldValidationErrorCode.TREE_MALFORMED
            )

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

        # Then run AppListField's validation to skip AppField's to_internal_value
        try:
            value = AppListField.to_internal_value(self, data)
            AppListField.run_validators(self, value)
        except Exception as e:
            return None

        # Process children recursively
        for node in value:
            children = node.get(Fields.CHILDREN)
            if children:
                node[Fields.CHILDREN] = self.children_field.run_validation(children)

        return value
