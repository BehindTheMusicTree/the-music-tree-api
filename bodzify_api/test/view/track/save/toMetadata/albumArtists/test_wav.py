#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_TRACK_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_longest(self):
        albumArtistsName = "a" * settings.ALBUM_ARTISTS_FIELD_MAX_CHAR
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: albumArtistsName
        }
        response = self.post_sample_track(sample_filename="sample.wav", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        albumArtistsKey = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.saved_track_metadata[albumArtistsKey] == albumArtistsName

    def test_null(self):
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: ""
        }
        response = self.post_sample_track(sample_filename="sample.wav", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        albumArtistsKey = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.saved_track_metadata[albumArtistsKey] in ["", None]