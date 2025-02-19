
from rest_framework.fields import ListField
from bodzify_api.serializer.field.AppField import AppField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class ArtistsNamesField(AppField, ListField):
    def to_internal_value(self, data):
        if not data:
            return None

        # Only accept array input
        if not isinstance(data, (list, tuple)):
            raise AppValidationError(
                field=self.get_error_field_name(),
                message='Multiple values must be sent using array notation (field[]=value)',
                field_validation_error_code=FieldValidationErrorCode.LIST_EXPECTED
            )

        # Check for empty values between commas
        if len(data) > 1:
            for artist_name in data:
                if artist_name is None or artist_name == '':
                    raise AppValidationError(
                        field=self.get_error_field_name(),
                        message='Empty artist names are not allowed when specifying multiple artists',
                        field_validation_error_code=FieldValidationErrorCode.ARTIST_NAME_EMPTY_IN_LIST
                    )

        # Check for duplicates
        unique_artists = set(data)
        if len(unique_artists) < len(data):
            raise AppValidationError(
                field=self.get_error_field_name(),
                message='Duplicate artist names are not allowed',
                field_validation_error_code=FieldValidationErrorCode.ARTIST_NAMES_DUPLICATE
            )

        # Convert tuple to list if necessary to match ListField's expected type
        list_data = list(data) if isinstance(data, tuple) else data
        return ListField.to_internal_value(self, list_data)
