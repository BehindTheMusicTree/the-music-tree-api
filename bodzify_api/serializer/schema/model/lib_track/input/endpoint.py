from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.field.PositionInAlbumField import PositionInAlbumField
from bodzify_api.serializer.field.RatingField import RatingField
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.field.ArtistsNamesField import ArtistsNamesField
from bodzify_api.serializer.field.criteria.GenreField import GenreField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from .Fields import Fields

ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be specified if album artists name is."""
POSITION_IN_ALBUM_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be specified if album position is."""


class LibTrackEndPointSerializer(AppSerializer):
    track_file_fingerprint_must_be_unique = serializers.BooleanField(required=False)
    title = AppCharField(max_length=settings.LIB_TRACK_TITLE_LEN_MAX,
                         required=False,
                         allow_blank=True,
                         allow_null=True)
    force_title_generation = serializers.BooleanField(required=False)
    artists_names = ArtistsNamesField(max_length=settings.ARTISTS_NAMES_LEN_MAX,
                                      required=False,
                                      allow_null=True)
    album_name = AppCharField(max_length=settings.ALBUM_NAME_LEN_MAX,
                              required=False,
                              allow_blank=True,
                              allow_null=True)
    album_artists_names = ArtistsNamesField(max_length=settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX,
                                            required=False,
                                            allow_null=True)
    position_in_album = PositionInAlbumField()

    genre_uuid = GenreField(required=False)
    genre_name = AppCharField(max_length=settings.CRITERIA_NAME_LEN_MAX,
                              required=False,
                              allow_blank=True,
                              allow_null=True)
    rating = RatingField()
    language = AppCharField(max_length=settings.LIB_TRACK_LANGUAGE_LEN_MAX,
                            required=False,
                            allow_blank=True,
                            allow_null=True)

    def validate(self, data):
        if Fields.GENRE_UUID in data and Fields.GENRE_NAME in data:
            if data[Fields.GENRE_UUID] not in ['', None] and data[Fields.GENRE_NAME] not in ['', None]:
                raise AppValidationError(
                    field=Fields.GENRE_NAME,
                    message='Genre name and genre uuid cannot be specified at the same time',
                    field_validation_error_code=FieldValidationErrorCode.MUTUALLY_EXCLUSIVE
                )

        if Fields.ALBUM_ARTISTS_NAMES_ARRAY in data:
            error_message = None
            if Fields.ALBUM_NAME not in data:
                error_message = ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE
            elif data[Fields.ALBUM_NAME] in [None, ""]:
                error_message = ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE

            if error_message:
                raise AppValidationError(
                    field=Fields.ALBUM_ARTISTS_NAMES_ARRAY,
                    message=error_message,
                    field_validation_error_code=FieldValidationErrorCode.DEPENDENCY_MISSING
                )

        if Fields.POSITION_IN_ALBUM in data:
            error_message = None
            if Fields.ALBUM_NAME not in data:
                error_message = POSITION_IN_ALBUM_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE
            elif data[Fields.ALBUM_NAME] in [None, ""]:
                error_message = POSITION_IN_ALBUM_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE

            if error_message:
                AppValidationError(
                    field=Fields.ALBUM_NAME,
                    message=error_message,
                    field_validation_error_code=FieldValidationErrorCode.DEPENDENCY_MISSING
                )

        return super().validate(data)
