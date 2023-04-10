#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class AlbumArtistsTestCase(ApiViewTestCase):

    def test_withCorrectSpacing(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": "Chuck",
            "albumArtistsName": "Chuck Berry,  The Beatles,The Rolling Stones "
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        albumArtistsKey = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.savedTrackMetadata[albumArtistsKey] == "Chuck Berry,The Beatles,The Rolling Stones"
