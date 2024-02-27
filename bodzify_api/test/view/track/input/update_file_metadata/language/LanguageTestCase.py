#!/usr/bin/env python

from bodzify_api import settings
import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.serializer.track.input.schema.LibTrackSchemaSaveSerializer import FIELDS as SAVE_FIELDS
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class LanguageTestCase(UpdateFileMetadataStrTestCase):
    save_field = SAVE_FIELDS.LANGUAGE
    lib_track_metadata_dict_key = AudioMetadataManager.METADATA_DICT_KEYS.LANGUAGE
    length_max = settings.LIB_TRACK_LANGUAGE_LENGTH_MAX


class LanguageMp3TestCase(LanguageTestCase):
    file_extension = 'mp3'


class LanguageFlacTestCase(LanguageTestCase):
    file_extension = 'flac'


class LanguageWavTestCase(LanguageTestCase):
    file_extension = 'wav'
