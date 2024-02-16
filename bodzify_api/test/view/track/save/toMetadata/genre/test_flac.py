#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_TRACK_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_longest(self):
        genre_name = "a" * settings.CRITERIA_NAME_LENGTH_MAX
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.GENRE_NAME: genre_name
        }
        response = self.post_sample_track(sample_filename="sample.flac", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        key = AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME
        assert self.saved_track_metadata[key] == genre_name

    def test_null(self):
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.GENRE_NAME: ""
        }
        response = self.post_sample_track(sample_filename="sample.flac", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        key = AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME
        assert self.saved_track_metadata[key] in ["", None]
