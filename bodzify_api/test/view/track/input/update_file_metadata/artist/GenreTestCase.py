#!/usr/bin/env python

from bodzify_api.settings import settings
import bodzify_api.utils.audiometadata as audiometadata
from bodzify_api.serializer.track.input.schema import FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class GenreTestCase(UpdateFileMetadataStrTestCase):
    save_field = SAVE_SCHEMA_FIELDS.GENRE_NAME
    lib_track_normalized_metadata_key = audiometadata.NormalizedMetadataKeys.GENRE_NAME
    length_max = settings.CRITERIA_NAME_LEN_MAX


class LanguageMp3TestCase(GenreTestCase):
    file_extension = 'mp3'


class LanguageFlacTestCase(GenreTestCase):
    file_extension = 'flac'


class LanguageWavTestCase(GenreTestCase):
    file_extension = 'wav'
