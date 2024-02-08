#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_TRACK_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_longest(self):
        albumName = "a" * settings.ALBUM_NAME_MAX_CHAR
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_NAME: albumName
        }
        response = self.post_sample_track(sample_filename="sample.flac", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        key = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME
        assert self.savedTrackMetadata[key] == albumName

    def test_null(self):
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_NAME: ""
        }
        response = self.post_sample_track(sample_filename="sample.flac", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        key = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME
        assert self.savedTrackMetadata[key]  in ["", None]