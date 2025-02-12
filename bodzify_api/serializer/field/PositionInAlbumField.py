from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.view.error.AppValidationError import AppValidationError
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


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
            raise AppValidationError.from_field(
                field='positionInAlbum',
                message='Position in album must be an integer',
                code=FieldValidationErrorCode.INVALID_FORMAT
            )

        if value is not None:
            if value < 1:
                raise AppValidationError.from_field(
                    field='positionInAlbum',
                    message='Position in album must be greater than or equal to 1',
                    code=FieldValidationErrorCode.POSITION_IN_ALBUM_TOO_SMALL
                )
            if value > settings.LIB_TRACK_POSITION_IN_ALBUM_MAX:
                raise AppValidationError.from_field(
                    field='positionInAlbum',
                    message=f'Position in album must be less than or equal to {settings.LIB_TRACK_POSITION_IN_ALBUM_MAX}',
                    code=FieldValidationErrorCode.POSITION_IN_ALBUM_TOO_LARGE
                )

        return value
