
import os
from typing import Any, cast
from django.core.files.base import File as DjangoFile

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.model.user.User import User
from bodzify_api.serializer.field.TrackFileField import TrackFileField
from bodzify_api.serializer.model.lib_track.input.input import LibTrackInputSerializer
from bodzify_api.utils import audio_metadata, data_transformer, utils
from bodzify_api.utils.audio_metadata.exceptions import FileCorruptedError
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey
from ..schema.Fields import Fields as SchemaFields
from .Fields import Fields as PostFields


class LibTrackPostSerializer(LibTrackInputSerializer):
    file = TrackFileField(required=True)

    def _get_track_filename_with_extension(self, track_file_url: str, **kwargs) -> tuple[str, bool]:
        file_extension = utils.get_file_extension_from_url(track_file_url)
        is_filename_randomly_generated = False
        if PostFields.TITLE in kwargs:
            title = kwargs[PostFields.TITLE]
            artists_names_list = kwargs.get(PostFields.ARTISTS_NAMES_ARRAY)
            if artists_names_list and len(artists_names_list) > 0:
                artists_names = ", ".join(artists_names_list)
                if artists_names is None or artists_names == "":
                    filename_without_extension = title
                else:
                    filename_without_extension = artists_names + " - " + title
            else:
                filename_without_extension = title
            filename_with_extension = filename_without_extension + "." + file_extension
        else:
            filename_with_extension = utils.get_substring_after_last_slash(track_file_url)
            if len(filename_with_extension) > settings.LIB_TRACK_FILENAME_LEN_MAX:
                filename_without_extension = utils.generate_short_uu(
                    settings.LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH - len(file_extension) - 1)
                filename_with_extension = filename_without_extension + "." + file_extension
                is_filename_randomly_generated = True
        return filename_with_extension, is_filename_randomly_generated

    def _get_generated_title_from_data(self, file: DjangoFile, data: dict):
        filename = os.path.basename(file.name).rsplit('.', 1)[0]
        filename = filename.rstrip()
        filename_without_expressions_to_exclude = data_transformer.remove_substrings_from_string(
            string_a=filename, substrings=settings.LIB_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE)

        if len(filename_without_expressions_to_exclude) > settings.LIB_TRACK_FILENAME_LEN_MAX:
            title = settings.LIB_TRACK_GENERATED_TITLE_PREFIXE + \
                utils.generate_short_uu(
                    settings.LIB_TRACK_GENERATED_TITLE_LENGTH - len(settings.LIB_TRACK_GENERATED_TITLE_PREFIXE))
        else:
            title = filename_without_expressions_to_exclude
        return title

    def _get_data_from_file(self, file, user: User):
        try:
            app_merged_metadata_dict = audio_metadata.get_merged_app_metadata(
                file=file, normalized_rating_max_value=settings.LIB_TRACK_RATING_VALUE_MAX)
        except FileCorruptedError as exc:
            raise AppValidationException(field_name=PostFields.TRACK_FILE_PUBLIC,
                                         message=str(exc),
                                         field_validation_error_code=FieldValidationErrorCode.FILE_CORRUPTED)

        schema_data_with_potential_none = data_transformer.get_copy_of_dict_including_only_specified_keys(
            data_dict=app_merged_metadata_dict,
            keys=[AppMetadataKey.TITLE,
                  AppMetadataKey.ARTISTS_NAMES,
                  AppMetadataKey.ALBUM_NAME,
                  AppMetadataKey.ALBUM_ARTISTS_NAMES,
                  AppMetadataKey.GENRE_NAME,
                  AppMetadataKey.RATING,
                  AppMetadataKey.LANGUAGE])

        metadata_max_lengths = {
            AppMetadataKey.TITLE: settings.LIB_TRACK_TITLE_LEN_MAX,
            AppMetadataKey.ARTISTS_NAMES: settings.ARTISTS_NAMES_LEN_MAX,
            AppMetadataKey.ALBUM_NAME: settings.ALBUM_NAME_LEN_MAX,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX,
            AppMetadataKey.GENRE_NAME: settings.CRITERIA_NAME_LEN_MAX,
            AppMetadataKey.LANGUAGE: settings.LANGUAGE_LEN_MAX,
        }
        for key, max_length in metadata_max_lengths.items():
            metadata_value = schema_data_with_potential_none.get(key)
            if metadata_value:
                if key.get_optional_type() == list[str]:
                    truncated_values = []
                    for value in metadata_value:
                        truncated_values.append(value[:max_length])
                    schema_data_with_potential_none[key] = truncated_values
                else:
                    schema_data_with_potential_none[key] = schema_data_with_potential_none[key][:max_length]

        genre_name = schema_data_with_potential_none.get(AppMetadataKey.GENRE_NAME)
        if genre_name:
            from bodzify_api.model.criteria.children.genre.Genre import Genre
            schema_data_with_potential_none[PostFields.GENRE] = Genre.objects.get_or_create(user=user, name=genre_name)[
                0]

        schema_data_clean = data_transformer.remove_none_or_empty_key_from_dict(schema_data_with_potential_none)
        schema_data_clean[SchemaFields.TRACK_FILE_PUBLIC] = file

        return schema_data_clean

    def _get_schema_data_from_post_data(self, user: User, **kwargs) -> dict[str, Any]:
        file = kwargs[PostFields.TRACK_FILE_PUBLIC]
        schema_data_from_file = self._get_data_from_file(file=file, user=user)

        schema_data = schema_data_from_file.copy()
        keys = [PostFields.TRACK_FILE_PUBLIC,
                PostFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE,
                PostFields.TITLE,
                PostFields.ARTISTS_NAMES_ARRAY,
                PostFields.ALBUM_NAME,
                PostFields.ALBUM_ARTISTS_NAMES_ARRAY,
                PostFields.TRACK_NUMBER,
                PostFields.GENRE,
                PostFields.RATING,
                PostFields.LANGUAGE]
        data_transformer.override_dict1_with_dict2_values_for_each_key_in_dict2(
            dict1=schema_data, dict2=kwargs, keys=keys)

        return schema_data

    def validate(self, data):
        user = self.context['request'].user
        data = self._get_schema_data_from_post_data(user=user, **data)

        # If title is not provided, generate it from the file
        if data.get(PostFields.TITLE) in [None, '']:
            file = cast(DjangoFile, data.get(PostFields.TRACK_FILE_PUBLIC))
            if isinstance(file, str):  # URL case
                # Get filename from URL
                filename, _ = self._get_track_filename_with_extension(
                    file,
                    title=data.get(PostFields.TITLE),
                    artists_names_array=data.get(PostFields.ARTISTS_NAMES_ARRAY)
                )
                # Remove extension to get title
                data[SchemaFields.TITLE] = os.path.splitext(filename)[0]
            else:  # File upload case
                data[SchemaFields.TITLE] = self._get_generated_title_from_data(file, data)

        return super().validate(data)
