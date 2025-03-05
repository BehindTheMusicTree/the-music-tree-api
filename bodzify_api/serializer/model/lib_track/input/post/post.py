
import os
from django.core.files.base import File as DjangoFile

from bodzify_api import settings
from bodzify_api.serializer.field.TrackFileField import TrackFileField
from bodzify_api.serializer.model.lib_track.input.input import LibTrackInputSerializer
from bodzify_api.utils import data_transformer, utils
from .Fields import Fields


class LibTrackPostSerializer(LibTrackInputSerializer):
    file = TrackFileField(required=True)

    def _get_track_filename_with_extension(self, track_file_url: str, **kwargs) -> tuple[str, bool]:
        file_extension = utils.get_file_extension_from_url(track_file_url)
        is_filename_randomly_generated = False
        if Fields.TITLE in kwargs:
            title = kwargs[Fields.TITLE]
            artists_names_list = kwargs.get(Fields.ARTISTS_NAMES_ARRAY)
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

    def validate(self, data):
        # If title is not provided, generate it from the file
        if Fields.TITLE not in data or data.get(Fields.TITLE) in [None, '']:
            file = data.get(Fields.TRACK_FILE_PUBLIC)
            if isinstance(file, str):  # URL case
                # Get filename from URL
                filename, _ = self._get_track_filename_with_extension(
                    file,
                    title=data.get(Fields.TITLE),
                    artists_names_array=data.get(Fields.ARTISTS_NAMES_ARRAY)
                )
                # Remove extension to get title
                data[Fields.TITLE] = os.path.splitext(filename)[0]
            else:  # File upload case
                data[Fields.TITLE] = self._get_generated_title_from_data(file, data)

        return super().validate(data)
