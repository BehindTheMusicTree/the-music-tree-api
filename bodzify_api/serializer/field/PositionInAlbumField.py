from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


class PositionInAlbumField(serializers.IntegerField):
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
            raise AppValidationException(
                field_name='positionInAlbum',
                message='Position in album must be an integer',
                field_validation_error_code=FieldValidationErrorCode.INVALID_FORMAT
            )

        if value is not None:
            if value < 1:
                raise AppValidationException(
                    field_name='positionInAlbum',
                    message='Position in album must be greater than or equal to 1',
                    field_validation_error_code=FieldValidationErrorCode.TRACK_NUMBER_TOO_SMALL
                )
            if value > settings.LIB_TRACK_TRACK_NUMBER_MAX:
                raise AppValidationException(
                    field_name='positionInAlbum',
                    message=f'Position in album must be less than or equal to {settings.LIB_TRACK_TRACK_NUMBER_MAX}',
                    field_validation_error_code=FieldValidationErrorCode.TRACK_NUMBER_TOO_LARGE
                )

        return value
