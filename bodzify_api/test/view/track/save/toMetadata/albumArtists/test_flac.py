#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class AlbumArtistsTestCase(TrackViewTestCase):

    def test_longest(self):
        albumArtistsName = "a" * settings.ALBUM_ARTISTS_FIELD_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/flac/0127.flac",
            "albumName": "Chuck",
            "albumArtistsName": albumArtistsName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        albumArtistsKey = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.savedTrackMetadata[albumArtistsKey] == albumArtistsName

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/flac/0127.flac",
            "albumName": "Chuck",
            "albumArtistsName": None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        albumArtistsKey = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.savedTrackMetadata[albumArtistsKey] in ["", None]