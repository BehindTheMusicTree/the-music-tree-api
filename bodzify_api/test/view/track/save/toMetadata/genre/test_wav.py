#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class WavTestCase(TrackViewTestCase):

    def test_longest(self):
        genreName = "a" * settings.CRITERIA_NAME_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "genreName": genreName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        genreNameKey = AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME
        assert self.savedTrackMetadata[genreNameKey] == genreName

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "genreName": None,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        genreNameKey = AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME
        assert self.savedTrackMetadata[genreNameKey] in ["", None]
