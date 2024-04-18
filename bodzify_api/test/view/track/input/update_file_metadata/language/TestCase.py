#!/usr/bin/env python

from bodzify_api import settings
import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.serializer.track.input.LibTrackSaveSchemaSerializer import FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):
    save_field = SAVE_SCHEMA_FIELDS.LANGUAGE
    lib_track_metadata_dict_key = AudioMetadataManager.METADATA_DICT_KEYS.LANGUAGE
    length_max = settings.LIB_TRACK_LANGUAGE_LENGTH_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
