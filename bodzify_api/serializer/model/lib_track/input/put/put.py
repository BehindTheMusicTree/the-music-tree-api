
from typing import Any
from rest_framework import serializers

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.serializer.model.lib_track.input.input import LibTrackInputSerializer
from bodzify_api.serializer.PutSerializer import PutSerializer
from .Fields import Fields


class LibTrackPutSerializer(PutSerializer, LibTrackInputSerializer):
    file = serializers.FileField(required=False)
    archived = serializers.BooleanField(required=False)

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        data = super(PutSerializer, self).validate(data)

        album_artists_names = data.get(Fields.ALBUM_ARTISTS_NAMES_ARRAY, None)
        if album_artists_names is not None:
            if not data.get(Fields.ALBUM_NAME, None):
                raise AppValidationException(message="Album name is required when album artists are provided",
                                             field_name=Fields.ALBUM_NAME,
                                             field_validation_error_code=FieldValidationErrorCode.DEPENDENCY_MISSING)
        else:
            if data.get(Fields.ALBUM_NAME, None):
                raise AppValidationException(message="Album artists are required when album name is provided",
                                             field_name=Fields.ALBUM_ARTISTS_NAMES_ARRAY,
                                             field_validation_error_code=FieldValidationErrorCode.DEPENDENCY_MISSING)

        return super(LibTrackInputSerializer, self).validate(data)
