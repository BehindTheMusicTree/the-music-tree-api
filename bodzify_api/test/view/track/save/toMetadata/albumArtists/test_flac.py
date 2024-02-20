#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_TRACK_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_longest(self):
        album_artistsName = "a" * settings.ALBUM_ARTISTS_FIELD_LENGTH_MAX
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: album_artistsName
        }
        response = self.post_sample_track(sample_filename="sample.flac", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        album_artistsKey = AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.saved_track_metadata[album_artistsKey] == album_artistsName

    def test_null(self):
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: ""
        }
        response = self.post_sample_track(sample_filename="sample.flac", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        album_artistsKey = AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.saved_track_metadata[album_artistsKey] in ["", None]