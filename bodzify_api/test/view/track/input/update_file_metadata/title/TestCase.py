#!/usr/bin/env python

from bodzify_api.settings import settings
import bodzify_api.utils.audiometadata as audiometadata
from bodzify_api.serializer.track.input.schema import FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):
    save_field = SAVE_SCHEMA_FIELDS.TITLE
    lib_track_normalized_metadata_key = audiometadata.NormalizedMetadataKeys.TITLE
    length_max = settings.LIB_TRACK_TITLE_LEN_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
