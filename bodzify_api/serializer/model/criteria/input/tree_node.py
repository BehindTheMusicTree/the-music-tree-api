from rest_framework.serializers import ListField, DictField, CharField

from bodzify_api.model.criteria.Fields import Fields
from bodzify_api.serializer.AppSerializer import AppSerializer


class CriteriaTreeNodeSerializer(AppSerializer):
    name = CharField(max_length=100, allow_blank=False)
    children = ListField(child=DictField(), required=False, default=list)

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise ValueError("Each node must be a dictionary")
        return super().to_internal_value(data)

    def validate_children(self, value):
        if not isinstance(value, list):
            raise ValueError(f"{Fields.CHILDREN} must be an array")
        from bodzify_api.serializer.model.criteria.input.tree_node import CriteriaTreeNodeSerializer
        for child in value:
            CriteriaTreeNodeSerializer(data=child).is_valid(raise_exception=True)
        return value
