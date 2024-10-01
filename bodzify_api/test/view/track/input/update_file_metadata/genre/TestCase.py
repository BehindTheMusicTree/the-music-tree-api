#!/usr/bin/env python

from bodzify_api import settings
import bodzify_api.utils.audio_metadata as audio_metadata
from bodzify_api.serializer.track.input.schema import Fields as SaveSchemaFields
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):
    save_field = SaveSchemaFields.GENRE_NAME
    lib_track_normalized_metadata_key = audio_metadata.NormalizedMetadataKeys.GENRE_NAME
    length_max = settings.CRITERIA_NAME_LEN_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
