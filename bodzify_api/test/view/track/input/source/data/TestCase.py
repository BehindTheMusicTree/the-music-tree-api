#!/usr/bin/env python

from bodzify_api import settings
import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.serializer.track.input.schema.LibTrackPostSchemaSerializer import FIELDS as POST_FIELDS
from bodzify_api.test.view.track.input.source.data.LibTrackAttributeFromDataTestCase import AttributeFromDataTestCase


class TestCase(AttributeFromDataTestCase):
    save_field = POST_FIELDS.ALBUM_ARTISTS_NAMES_STRING
    lib_track_metadata_dict_key = AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
    length_max = settings.ALBUM_ARTISTS_FIELD_LENGTH_MAX
    album_data_json = {
        POST_FIELDS.ALBUM_NAME: "The Great Twenty-Eight",
    }

    def test_on_missing_tag_then_ok(self):
        self._test_value("a", additional_data_json=self.album_data_json, file_has_tags=False)

    def test_on_present_tag_then_ok(self):
        self._test_value("a", additional_data_json=self.album_data_json, file_has_tags=True)

    def test_longest_then_ok(self):
        self._test_value("a" * self.length_max, additional_data_json=self.album_data_json, file_has_tags=False)


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
