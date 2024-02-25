#!/usr/bin/env python

from rest_framework import status

import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.serializer.track.input.schema.LibTrackSchemaSaveSerializer import FIELDS as SAVE_FIELDS
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_flac(self):
        album_artists_names_str = "Chuck Berry,  The Beatles,The Rolling Stones "
        data = {
            SAVE_FIELDS.ALBUM_NAME: "Chuck",
            SAVE_FIELDS.ALBUM_ARTISTS_NAMES_STRING: album_artists_names_str
        }
        response = self.post_lib_track_with_generic_sample_no_tags(generic_sample_extension='flac', data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        album_artistsKey = AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.saved_lib_track_metadata[album_artistsKey] == "Chuck Berry,The Beatles,The Rolling Stones"

    def test_mp3(self):
        album_artists_names_str = "Chuck Berry,  The Beatles,The Rolling Stones "
        data = {
            SAVE_FIELDS.ALBUM_NAME: "Chuck",
            SAVE_FIELDS.ALBUM_ARTISTS_NAMES_STRING: album_artists_names_str
        }
        response = self.post_lib_track_with_generic_sample_no_tags(generic_sample_extension='mp3', data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        album_artistsKey = AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.saved_lib_track_metadata[album_artistsKey] == "Chuck Berry,The Beatles,The Rolling Stones"

    def test_wav(self):
        album_artists_names_str = "Chuck Berry,  The Beatles,The Rolling Stones "
        data = {
            SAVE_FIELDS.ALBUM_NAME: "Chuck",
            SAVE_FIELDS.ALBUM_ARTISTS_NAMES_STRING: album_artists_names_str
        }
        response = self.post_lib_track_with_generic_sample_no_tags(generic_sample_extension='wav', data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        album_artistsKey = AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.saved_lib_track_metadata[album_artistsKey] == "Chuck Berry,The Beatles,The Rolling Stones"
