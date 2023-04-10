#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class AlbumArtistsTestCase(ApiViewTestCase):

    def test_longest(self):
        artistName = "a" * settings.ARTIST_NAME_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/flac/0127.flac",
            "artistName": artistName,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        artistNameKey = AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME
        assert self.savedTrackMetadata[artistNameKey] == artistName

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/flac/0127.flac",
            "artistName": None,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        artistNameKey = AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME
        assert self.savedTrackMetadata[artistNameKey] in ["", None]