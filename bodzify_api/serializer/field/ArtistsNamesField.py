
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.schema.model.lib_track.input.Fields import Fields


class ArtistsNamesField(AppCharField):
    def to_internal_value(self, data):
        if not data:
            return None

        # Only accept array input
        if not isinstance(data, (list, tuple)):
            raise AppValidationError(
                field=Fields.ARTISTS_NAMES,
                message='Multiple values must be sent using array notation (field[]=value)',
                code=FieldValidationErrorCode.LIST_EXPECTED
            )

        artists = [str(artist).strip() for artist in data]

        # Check for empty values between commas
        if '' in artists and len(artists) > 1:
            raise AppValidationError(
                field=Fields.ARTISTS_NAMES,
                message='Empty artist names are not allowed when specifying multiple artists',
                code=FieldValidationErrorCode.ARTIST_NAME_EMPTY_IN_LIST
            )

        # Check for duplicates
        unique_artists = set(artists)
        if len(unique_artists) < len(artists):
            raise AppValidationError(
                field=Fields.ARTISTS_NAMES,
                message='Duplicate artist names are not allowed',
                code=FieldValidationErrorCode.ARTIST_NAMES_DUPLICATE
            )

        # Sort artists for consistent ordering
        sorted_artists = sorted(artists)
        return ', '.join(sorted_artists)
