#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class WavTestCase(ApiViewTestCase):

    def test_longest(self):
        language = "a" * settings.TRACK_LANGUAGE_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "language": language
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        languageKey = AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE
        assert self.savedTrackMetadata[languageKey] == language

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "language": None,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        languageKey = AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE
        assert self.savedTrackMetadata[languageKey] in ["", None]
