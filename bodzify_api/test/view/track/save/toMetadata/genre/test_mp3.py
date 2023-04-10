#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class Mp3TestCase(ApiViewTestCase):

    def test_longest(self):
        genreName = "a" * settings.CRITERIA_NAME_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/mp3/0037.mp3",
            "genreName": genreName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        genreNameKey = AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME
        assert self.savedTrackMetadata[genreNameKey] == genreName

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/mp3/0037.mp3",
            "genreName": None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        genreNameKey = AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME
        assert self.savedTrackMetadata[genreNameKey] in ["", None]
