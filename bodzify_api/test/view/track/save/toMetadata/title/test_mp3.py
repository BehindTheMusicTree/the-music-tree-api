#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class Mp3TestCase(ApiViewTestCase):

    def test_longest(self):
        title = "a" * settings.TRACK_TITLE_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/mp3/0037.mp3",
            "title": title
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        titleKey = AudioMetadataService.METADATA_DICT_KEYS.TITLE
        assert self.savedTrackMetadata[titleKey] == title

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/mp3/0037.mp3",
            "title": None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        titleKey = AudioMetadataService.METADATA_DICT_KEYS.TITLE
        assert self.savedTrackMetadata[titleKey] in ["", None]
