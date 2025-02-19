from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class RatingField(serializers.IntegerField):
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
            raise AppValidationError(
                field_name='rating',
                message='Rating must be an integer',
                field_validation_error_code=FieldValidationErrorCode.INVALID_FORMAT
            )

        if value is not None:
            if value < 0:
                raise AppValidationError(
                    field_name='rating',
                    message='Rating must be greater than or equal to 0',
                    field_validation_error_code=FieldValidationErrorCode.RATING_TOO_SMALL
                )
            if value > settings.LIB_TRACK_RATING_VALUE_MAX:
                raise AppValidationError(
                    field_name='rating',
                    message=f'Rating must be less than or equal to {settings.LIB_TRACK_RATING_VALUE_MAX}',
                    field_validation_error_code=FieldValidationErrorCode.RATING_TOO_LARGE
                )

        return value
