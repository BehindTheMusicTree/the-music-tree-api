from rest_framework.serializers import ListField, DictField

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.model.criteria.input.tree_node import CriteriaTreeNodeSerializer


class CriteriaTreeImportSerializer(AppSerializer):
    data: ListField = ListField(child=DictField())

    def to_internal_value(self, data):
        if isinstance(data, list):
            return {'data': data}
        return super().to_internal_value(data)

    def validate_data(self, value):
        if not value:
            raise AppValidationException(field_name="data",
                                         message="At least one criteria must be provided",
                                         field_validation_error_code=FieldValidationErrorCode.REQUIRED)
        for node in value:
            CriteriaTreeNodeSerializer(data=node).is_valid(raise_exception=True)
        return value
