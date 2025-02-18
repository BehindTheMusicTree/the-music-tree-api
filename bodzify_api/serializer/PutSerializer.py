from typing import Dict, Any

from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class PutSerializer(AppValidationSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        attrs = super().validate(attrs)

        # Ensure there's at least one field to update
        request = self.context.get('request')
        if request and request.method.upper() == 'PUT' and not attrs:
            raise AppValidationError(
                field='request',
                message='At least one field must be provided for update',
                code=FieldValidationErrorCode.NO_UPDATES
            )

        return super().validate(attrs)
