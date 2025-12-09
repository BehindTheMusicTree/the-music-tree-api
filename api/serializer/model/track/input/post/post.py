
import os
from typing import cast
from django.core.files.base import File as DjangoFile

from api import settings
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.exception.validation.app.AppValidationException import AppValidationException
from api.model.user.User import User
from api.serializer.model.track.input.Fields import Fields
from api.serializer.model.track.input.input import TrackInputSerializer
from api.utils import audio_file_metadata, data_transformer, utils
from api.utils.audio_file_metadata.exceptions import FileCorruptedError
from api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey


class TrackPostSerializer(TrackInputSerializer):
    def _get_generated_title_from_data(self, data: dict):
        title = settings.UPLOADED_TRACK_GENERATED_TITLE_PREFIXE + \
            utils.generate_short_uu(
                settings.UPLOADED_TRACK_GENERATED_TITLE_LENGTH - len(settings.UPLOADED_TRACK_GENERATED_TITLE_PREFIXE))
        return title

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
            from api.model.criteria.children.genre.Genre import Genre
            input_data[Fields.GENRE] = Genre.objects.get_or_create(user=user, name=genre_name)[0]

    def validate(self, data: dict):
        self._validate_album_fields_from_data(data)

        user = self.context['request'].user

        keys = [Fields.TITLE,
                Fields.ARTISTS_NAMES,
                Fields.ALBUM_NAME,
                Fields.ALBUM_ARTISTS_NAMES,
                Fields.TRACK_NUMBER,
                Fields.GENRE,
                Fields.RATING,
                Fields.LANGUAGE]

        input_data = data.copy()

        if input_data.get(Fields.TITLE) in [None, '']:
            input_data[Fields.TITLE] = self._get_generated_title_from_data(input_data)

        return super().validate(input_data)
