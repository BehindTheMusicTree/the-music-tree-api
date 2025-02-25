from typing import Any, Dict

from bodzify_api.exception.validation.app.AppValidationError import \
    AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import \
    FieldValidationErrorCode
from bodzify_api.serializer.AppSerializer import AppSerializer


class PutSerializer(AppSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        attrs = super().validate(attrs)

        # Ensure there's at least one field to update
        request = self.context.get(self.REQUEST_FIELD)
        if request and request.method.upper() == 'PUT' and not attrs:
            raise AppValidationException(
                field_name=self.REQUEST_FIELD,
                message='At least one field must be provided for update',
                field_validation_error_code=FieldValidationErrorCode.NO_UPDATES
            )

        return super().validate(attrs)
