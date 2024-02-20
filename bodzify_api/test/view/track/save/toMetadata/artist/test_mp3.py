#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_TRACK_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_longest(self):
        artist_name = "a" * settings.TRACK_LANGUAGE_LENGTH_MAX
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ARTIST_NAME: artist_name
        }
        response = self.post_sample_track(sample_filename="sample.mp3", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        key = AudioMetadataManager.METADATA_DICT_KEYS.ARTIST_NAME
        assert self.saved_track_metadata[key] == artist_name

    def test_null(self):
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ARTIST_NAME: ""
        }
        response = self.post_sample_track(sample_filename="sample.mp3", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        key = AudioMetadataManager.METADATA_DICT_KEYS.ARTIST_NAME
        assert self.saved_track_metadata[key] in ["", None]
