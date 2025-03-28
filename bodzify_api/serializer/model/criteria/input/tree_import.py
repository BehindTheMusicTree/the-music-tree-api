from rest_framework.serializers import ListField, DictField

from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.model.criteria.input.tree_node import CriteriaTreeNodeSerializer


class CriteriaTreeImportSerializer(AppSerializer):
    data = ListField(child=DictField(), allow_empty=False)

    def to_internal_value(self, data):
        if isinstance(data, list):
            return {'data': data}
        return super().to_internal_value(data)

    def validate_data(self, value):
        if not value:
            raise ValueError("At least one criteria must be provided")
        for node in value:
            CriteriaTreeNodeSerializer(data=node).is_valid(raise_exception=True)
        return value
