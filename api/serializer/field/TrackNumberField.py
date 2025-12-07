from rest_framework import serializers

from api import settings
from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.field.AppField import AppField


class TrackNumberField(AppField, serializers.IntegerField):
    def __init__(self, **kwargs):
        kwargs['required'] = False
        kwargs['allow_null'] = True
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data == '':
            return None

        try:
            value = int(data)
        except (TypeError, ValueError):
            raise AppValidationException(field_name=self.get_error_field_name(),
                                         message='Position in album must be an integer',
                                         field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID)

        if value is not None:
            if value < 1:
                raise AppValidationException(
                    field_name=self.get_error_field_name(),
                    message='Position in album must be greater than or equal to 1',
                    field_validation_error_code=FieldValidationErrorCode.TRACK_NUMBER_TOO_SMALL)
            if value > settings.UPLOADED_TRACK_TRACK_NUMBER_MAX:
                raise AppValidationException(
                    field_name=self.get_error_field_name(),
                    message=f'Position in album must be less than or equal to {settings.UPLOADED_TRACK_TRACK_NUMBER_MAX}',
                    field_validation_error_code=FieldValidationErrorCode.TRACK_NUMBER_TOO_LARGE)

        return value
