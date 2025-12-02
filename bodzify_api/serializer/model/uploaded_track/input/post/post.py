
import os
from typing import cast
from django.core.files.base import File as DjangoFile

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.model.user.User import User
from bodzify_api.serializer.field.TrackFileField import TrackFileField
from bodzify_api.serializer.model.uploaded_track.input.Fields import Fields
from bodzify_api.serializer.model.uploaded_track.input.input import UploadedTrackInputSerializer
from bodzify_api.utils import audio_metadata, data_transformer, utils
from bodzify_api.utils.audio_metadata.exceptions import FileCorruptedError
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey
from .Fields import Fields as PostFields


class UploadedTrackPostSerializer(UploadedTrackInputSerializer):
    file = TrackFileField(required=True)

    def _get_generated_title_from_data(self, file: DjangoFile, data: dict):
        filename = os.path.basename(file.name).rsplit('.', 1)[0]
        filename = filename.rstrip()
        filename_without_expressions_to_exclude = data_transformer.remove_substrings_from_string(
            string_a=filename, substrings=settings.UPLOADED_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE)

        if len(filename_without_expressions_to_exclude) > settings.UPLOADED_TRACK_FILENAME_LEN_MAX:
            title = settings.UPLOADED_TRACK_GENERATED_TITLE_PREFIXE + \
                utils.generate_short_uu(
                    settings.UPLOADED_TRACK_GENERATED_TITLE_LENGTH - len(settings.UPLOADED_TRACK_GENERATED_TITLE_PREFIXE))
        else:
            title = filename_without_expressions_to_exclude
        return title

    def _get_metadata_from_file(self, file) -> dict:
        try:
            return audio_metadata.get_merged_app_metadata(
                file=file, normalized_rating_max_value=settings.UPLOADED_TRACK_RATING_VALUE_MAX)
        except FileCorruptedError as exc:
            raise AppValidationException(field_name=PostFields.TRACK_FILE_PUBLIC,
                                         message=str(exc),
                                         field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_CORRUPTED)

    def _truncate_metadata_values(self, metadata_dict: dict) -> dict:
        metadata_str_max_lengths = {
            AppMetadataKey.TITLE: settings.UPLOADED_TRACK_TITLE_LEN_MAX,
            AppMetadataKey.ARTISTS_NAMES: settings.ARTISTS_NAMES_LEN_MAX,
            AppMetadataKey.ALBUM_NAME: settings.ALBUM_NAME_LEN_MAX,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX,
            AppMetadataKey.GENRE_NAME: settings.CRITERIA_NAME_LEN_MAX,
            AppMetadataKey.LANGUAGE: settings.LANGUAGE_LEN_MAX,
        }

        for key, max_length in metadata_str_max_lengths.items():
            metadata_value = cast(str, metadata_dict.get(key))
            if metadata_value:
                if key.get_optional_type() == list[str]:
                    truncated_values = []
                    for value in metadata_value:
                        truncated_values.append(value[:max_length])
                    metadata_dict[key] = truncated_values
                else:
                    metadata_dict[key] = metadata_value[:max_length]

        return metadata_dict

    def _extract_metadata_fields(self, metadata_dict: dict) -> dict:
        data = data_transformer.get_copy_of_dict_including_only_specified_keys(
            data_dict=metadata_dict,
            keys=[Fields.TITLE,
                  Fields.ARTISTS_NAMES,
                  Fields.RATING,
                  Fields.LANGUAGE])
        if metadata_dict.get(Fields.ALBUM_NAME, None) not in [None, ""]:
            data[Fields.ALBUM_NAME] = metadata_dict.get(AppMetadataKey.ALBUM_NAME, None)
            data[Fields.ALBUM_ARTISTS_NAMES] = metadata_dict.get(AppMetadataKey.ALBUM_ARTISTS_NAMES, [])
        return data

    def _handle_genre(self, input_data: dict, file_metadata: dict, user: User):
        genre_name = file_metadata.get(AppMetadataKey.GENRE_NAME)
        if genre_name:
            from bodzify_api.model.criteria.children.genre.Genre import Genre
            input_data[PostFields.GENRE] = Genre.objects.get_or_create(user=user, name=genre_name)[0]

    def _get_input_data_from_file(self, file, user: User):
        file_metadata = self._get_metadata_from_file(file)
        file_metadata = self._truncate_metadata_values(file_metadata)

        input_data = self._extract_metadata_fields(file_metadata)
        self._handle_genre(user=user, input_data=input_data, file_metadata=file_metadata)

        input_data_clean = data_transformer.remove_none_or_empty_key_from_dict(input_data)
        input_data_clean[Fields.TRACK_FILE_INTERNAL] = file

        return input_data_clean

    def validate(self, data: dict):
        self._validate_album_fields_from_data(data)

        user = self.context['request'].user
        file = cast(DjangoFile, data.get(PostFields.TRACK_FILE_PUBLIC))  # Required so not None
        input_data = self._get_input_data_from_file(file=file, user=user)

        keys = [PostFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE,
                PostFields.TITLE,
                PostFields.ARTISTS_NAMES,
                PostFields.ALBUM_NAME,
                PostFields.ALBUM_ARTISTS_NAMES,
                PostFields.TRACK_NUMBER,
                PostFields.GENRE,
                PostFields.RATING,
                PostFields.LANGUAGE]
        data_transformer.override_dict1_with_dict2_values_for_each_key_in_dict2(dict1=input_data, dict2=data, keys=keys)

        input_data[Fields.TRACK_FILE_INTERNAL] = data[PostFields.TRACK_FILE_PUBLIC]

        # If title is not provided, generate it from the file
        if input_data.get(PostFields.TITLE) in [None, '']:
            input_data[PostFields.TITLE] = self._get_generated_title_from_data(file, input_data)

        return super().validate(input_data)
