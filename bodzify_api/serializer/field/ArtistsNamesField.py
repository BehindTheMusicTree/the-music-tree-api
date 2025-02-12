from rest_framework import serializers

from bodzify_api.view.error.AppValidationError import AppValidationError
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.schema.model.lib_track.input.Fields import Fields


class ArtistsNamesField(serializers.CharField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if not value:
            return value

        # Split by comma and strip whitespace
        artists = [artist.strip() for artist in value.split(',')]

        # Check for empty values between commas
        if '' in artists and len(artists) > 1:
            raise AppValidationError.from_field(
                field=Fields.ARTISTS_NAMES,
                message='Empty artist names are not allowed when specifying multiple artists',
                code=FieldValidationErrorCode.FIELD_ARTIST_NAME_EMPTY_IN_LIST
            )

        # Check for duplicates
        unique_artists = set(artists)
        if len(unique_artists) < len(artists):
            raise AppValidationError.from_field(
                field=Fields.ARTISTS_NAMES,
                message='Duplicate artist names are not allowed',
                code=FieldValidationErrorCode.FIELD_ARTIST_NAMES_DUPLICATE
            )

        # Sort artists for consistent ordering
        sorted_artists = sorted(artists)
        return ', '.join(sorted_artists)
