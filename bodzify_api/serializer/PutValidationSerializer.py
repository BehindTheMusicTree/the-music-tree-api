from typing import Dict, Any
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.ValidationResponseCode import ValidationResponseCode
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer


class PutValidationSerializer(AppValidationSerializer):
    """
    Serializer for PUT requests that enforces at least one field must be provided for updates.
    Inherits all validation functionality from AppValidationSerializer and adds PUT-specific validation.
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
            raise_validation_error(
                message='At least one field must be provided for update',
                code=ValidationResponseCode.FIELD_NO_UPDATES,
                field='request'
            )

        return attrs