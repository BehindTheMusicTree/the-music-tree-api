#!/usr/bin/env python
from rest_framework import status

import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_TRACK_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_withCorrectSpacing(self):
        album_artists_name = "Chuck Berry,  The Beatles,The Rolling Stones "
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: album_artists_name
        }
        response = self.post_sample_track(
            sample_filename="sample.mp3", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        album_artistsKey = AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.saved_track_metadata[album_artistsKey] == "Chuck Berry,The Beatles,The Rolling Stones"
