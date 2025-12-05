from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.user.User import User
from bodzify_api.serializer.AppInputSerializer import AppInputSerializer
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.field.ArtistsNamesField import ArtistsNamesField
from bodzify_api.serializer.field.TrackNumberField import TrackNumberField
from bodzify_api.serializer.field.RatingField import RatingField
from bodzify_api.serializer.field.criteria.CriteriaFieldInputType import CriteriaFieldInputType
from bodzify_api.serializer.field.criteria.GenreField import GenreField
from bodzify_api.model.uploaded_track.Fields import Fields as ModelFields
from bodzify_api.utils import data_transformer
from .Fields import Fields


class UploadedTrackInputSerializer(AppInputSerializer):
    track_file_fingerprint_must_be_unique = serializers.BooleanField(required=False)
    title = AppCharField(
        max_length=settings.UPLOADED_TRACK_TITLE_LEN_MAX, required=False, allow_blank=False, allow_null=True)
    force_title_generation = serializers.BooleanField(required=False)
    artists_names = ArtistsNamesField(max_length=settings.ARTISTS_NAMES_LEN_MAX, required=False, allow_null=True)
    album_name = AppCharField(max_length=settings.ALBUM_NAME_LEN_MAX, required=False, allow_blank=True, allow_null=True)
    album_artists_names = ArtistsNamesField(
        max_length=settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX, required=False, allow_null=True)
    track_number = TrackNumberField()
    genre = GenreField(
        input_types=[CriteriaFieldInputType.UUID, CriteriaFieldInputType.NAME], required=False, allow_null=True)
    rating = RatingField()
    language = AppCharField(
        max_length=settings.LANGUAGE_LEN_MAX, required=False, allow_blank=True, allow_null=True)

    def _update_model_data_with_album_if_name(self, user: User, data: dict):
        from bodzify_api.model.album.Album import Album
        album_name = data.pop(Fields.ALBUM_NAME, None)
        album_artists_names = data.pop(Fields.ALBUM_ARTISTS_NAMES, [])
        if album_name is not None:
            if album_name == "":
                data[ModelFields.ALBUM] = None
            else:
                album = Album.objects.get_album_from_name_and_album_artists_names_after_potential_creations(
                    user=user, name=album_name, album_artists_names=album_artists_names)
                data[ModelFields.ALBUM] = album

    def _update_data_with_artists_if_names_otherwise_empty_list(self, user: User, data: dict) -> None:
        if Fields.ARTISTS_NAMES in data:
            artists_names = data.pop(Fields.ARTISTS_NAMES) or []
            artists = Artist.objects.get_artists_list_from_names_after_potential_creation(
                user=user, artists_names=artists_names)
            data[ModelFields.ARTISTS] = artists

    def _validate_album_fields_from_data(self, data: dict):
        if Fields.ALBUM_ARTISTS_NAMES in data:
            if data.get(Fields.ALBUM_ARTISTS_NAMES) not in [None, []] and \
                    data.get(Fields.ALBUM_NAME, None) in [None, ""]:
                raise AppValidationException(message="Album name is required when album artists field is provided",
                                             field_name=Fields.ALBUM_NAME,
                                             field_validation_error_code=FieldValidationErrorCode.DEPENDENCY_MISSING)

        if Fields.TRACK_NUMBER in data and data.get(
                Fields.TRACK_NUMBER) is not None and data.get(
                Fields.ALBUM_NAME) in [
                None, ""]:
            raise AppValidationException(field_name=Fields.ALBUM_NAME,
                                         message="Album name must be specified if track position is.",
                                         field_validation_error_code=FieldValidationErrorCode.DEPENDENCY_MISSING)

    def validate(self, data: dict,):
        if Fields.LANGUAGE in data and data[Fields.LANGUAGE] == "":
            data[Fields.LANGUAGE] = None
        data_transformer.update_dict_converting_str_to_int_value_if_set(key=ModelFields.RATING, data=data)

        user = self.context['request'].user
        data[ModelFields.USER] = user

        self._update_data_with_artists_if_names_otherwise_empty_list(user=user, data=data)
        self._update_model_data_with_album_if_name(user=user, data=data)

        return super().validate(data)
