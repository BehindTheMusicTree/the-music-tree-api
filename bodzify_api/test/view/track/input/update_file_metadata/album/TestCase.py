#!/usr/bin/env python

from bodzify_api import settings
import bodzify_api.audiometadata as audiometadata
from bodzify_api.serializer.track.input.LibTrackSchemaSerializer import FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):
    save_field = SAVE_SCHEMA_FIELDS.ALBUM_NAME
    lib_track_metadata_dict_key = audiometadata.METADATA_DICT_KEYS.ALBUM_NAME
    length_max = settings.ALBUM_NAME_LENGTH_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
