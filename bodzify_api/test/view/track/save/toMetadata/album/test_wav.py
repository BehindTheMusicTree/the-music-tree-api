#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class AlbumArtistsTestCase(ApiViewTestCase):

    def test_longest(self):
        albumName = "a" * settings.ALBUM_NAME_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": albumName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        albumNameKey = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME
        assert self.savedTrackMetadata[albumNameKey] == albumName

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": None,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        albumNameKey = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME
        assert self.savedTrackMetadata[albumNameKey] in ["", None]
