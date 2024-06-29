#!/usr/bin/env python

from bodzify_api import settings
import bodzify_api.utils.audio_metadata as audio_metadata
from bodzify_api.serializer.track.input.endpoint.post import FIELDS as POST_FIELDS
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):
    save_field = POST_FIELDS.ALBUM_ARTISTS_NAMES_STR
    lib_track_normalized_metadata_key = audio_metadata.NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES
    length_max = settings.ALBUM_ARTISTS_FIELD_LEN_MAX
    album_data_dict = {
        POST_FIELDS.ALBUM_NAME: "The Great Twenty-Eight",
    }

    def test_on_missing_tag_then_ok(self):
        self._test_value("a", additional_data_dict=self.album_data_dict, file_has_tags=False)

    def test_on_present_tag_then_ok(self):
        self._test_value("a", additional_data_dict=self.album_data_dict, file_has_tags=True)

    def test_longest_then_ok(self):
        self._test_value("a" * self.length_max, additional_data_dict=self.album_data_dict, file_has_tags=False)


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
