#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class Mp3TestCase(TrackViewTestCase):

    def test_longest(self):
        language = "a" * settings.TRACK_LANGUAGE_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/mp3/0037.mp3",
            "language": language
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        languageKey = AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE
        assert self.savedTrackMetadata[languageKey] == language

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/mp3/0037.mp3",
            "language": None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        languageKey = AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE
        assert self.savedTrackMetadata[languageKey] in ["", None]
