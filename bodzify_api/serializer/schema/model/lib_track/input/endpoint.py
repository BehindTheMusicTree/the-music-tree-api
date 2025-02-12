from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.serializer.field.PositionInAlbumField import PositionInAlbumField
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from bodzify_api.serializer.field.ArtistsNamesField import ArtistsNamesField
from bodzify_api.serializer.field.criteria.GenreField import GenreField
from bodzify_api.view.error.AppValidationError import AppValidationError
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode
from .Fields import Fields

ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be specified if album artists name is."""
POSITION_IN_ALBUM_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be specified if album position is."""


class LibTrackEndPointSerializer(AppValidationSerializer):
    track_file_fingerprint_must_be_unique = serializers.BooleanField(required=False)
    title = serializers.CharField(max_length=settings.LIB_TRACK_TITLE_LEN_MAX,
                                  required=False,
                                  allow_blank=True,
                                  allow_null=True)
    force_title_generation = serializers.BooleanField(required=False)
    artists_names = ArtistsNamesField(max_length=settings.ARTISTS_NAMES_LEN_MAX,
                                      required=False,
                                      allow_blank=True,
                                      allow_null=True)
    album_name = serializers.CharField(max_length=settings.ALBUM_NAME_LEN_MAX,
                                       required=False,
                                       allow_blank=True,
                                       allow_null=True)
    album_artists_names = ArtistsNamesField(max_length=settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX,
                                            required=False,
                                            allow_blank=True,
                                            allow_null=True)
    position_in_album = PositionInAlbumField()

    genre_uuid = GenreField(required=False)
    genre_name = serializers.CharField(max_length=settings.CRITERIA_NAME_LEN_MAX,
                                       required=False,
                                       allow_blank=True,
                                       allow_null=True)
    rating = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    language = serializers.CharField(max_length=settings.LIB_TRACK_LANGUAGE_LEN_MAX,
                                     required=False,
                                     allow_blank=True,
                                     allow_null=True)

    def validate(self, data):
        if Fields.GENRE_UUID in data and Fields.GENRE_NAME in data:
            if data[Fields.GENRE_UUID] not in ['', None] and data[Fields.GENRE_NAME] not in ['', None]:
                raise AppValidationError.from_serializer(
                    field=Fields.GENRE_NAME,
                    message='Genre name and genre uuid cannot be specified at the same time',
                    code=FieldValidationErrorCode.FIELD_MUTUALLY_EXCLUSIVE
                )

        if Fields.ALBUM_ARTISTS_NAMES in data:
            error_message = None
            if Fields.ALBUM_NAME not in data:
                error_message = ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE
            elif data[Fields.ALBUM_NAME] in [None, ""]:
                error_message = ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE

            if error_message:
                raise AppValidationError.from_serializer(
                    field=Fields.ALBUM_ARTISTS_NAMES,
                    message=error_message,
                    code=FieldValidationErrorCode.FIELD_DEPENDENCY_MISSING
                )

        if Fields.POSITION_IN_ALBUM in data:
            error_message = None
            if Fields.ALBUM_NAME not in data:
                error_message = POSITION_IN_ALBUM_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE
            elif data[Fields.ALBUM_NAME] in [None, ""]:
                error_message = POSITION_IN_ALBUM_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE

            if error_message:
                raise AppValidationError.from_serializer(
                    field=Fields.ALBUM_NAME,
                    message=error_message,
                    code=FieldValidationErrorCode.FIELD_DEPENDENCY_MISSING
                )

        if Fields.RATING in data:
            value = data[Fields.RATING]
            if value and value != '':
                try:
                    value = int(value)
                except ValueError:
                    raise AppValidationError.from_serializer(
                        field=Fields.RATING,
                        message='Rating must be an integer',
                        code=FieldValidationErrorCode.FIELD_INVALID_FORMAT
                    )

        return super().validate(data)
