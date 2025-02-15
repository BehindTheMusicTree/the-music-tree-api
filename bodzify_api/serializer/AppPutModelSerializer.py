from typing import Dict, Any

from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.AppModelSerializer import AppModelSerializer


class AppPutModelSerializer(AppModelSerializer):
    """
    Model serializer for PUT requests that enforces at least one field must be provided for updates.
    Inherits all validation functionality from AppModelSerializer and adds PUT-specific validation.
    """

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the input data for PUT requests.
        Ensures that at least one field is provided for update.
        """
        # First run parent validations
        attrs = super().validate(attrs)

        # For PUT requests, ensure there's at least one field to update
        request = self.context.get('request')
        if request and request.method.upper() == 'PUT' and not attrs:
            raise AppValidationError(
                field='request',
                message='At least one field must be provided for update',
                code=FieldValidationErrorCode.NO_UPDATES
            )

        return attrs