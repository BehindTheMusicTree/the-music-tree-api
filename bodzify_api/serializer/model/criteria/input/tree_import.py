from rest_framework.serializers import ListField, DictField

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.model.criteria.input.tree_node import CriteriaTreeNodeSerializer


class CriteriaTreeImportSerializer(AppSerializer):
    data: ListField = ListField(child=DictField(), allow_empty=False)

    def to_internal_value(self, data):
        if isinstance(data, list):
            if not data:
                raise AppValidationException(field_name="data",
                                             message="At least one criteria must be provided",
                                             field_validation_error_code=FieldValidationErrorCode.REQUIRED)
            return {'data': data}
        raise AppValidationException(field_name="data",
                                     message="Input must be an array",
                                     field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID)

    def validate_data(self, value):
        for node in value:
            CriteriaTreeNodeSerializer(data=node).is_valid(raise_exception=True)
        return value
