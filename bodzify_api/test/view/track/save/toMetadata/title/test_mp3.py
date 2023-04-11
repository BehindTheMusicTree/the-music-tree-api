#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TestCase(ApiViewTestCase):

    def test_longest(self):
        title = "a" * settings.TRACK_TITLE_MAX_CHAR
        data = {
            "title": title
        }
        response = self.postSampleTrack(sampleFilename="sample.mp3", dataJson=data)
        assert response.status_code == status.HTTP_201_CREATED
        titleKey = AudioMetadataService.METADATA_DICT_KEYS.TITLE
        assert self.savedTrackMetadata[titleKey] == title

    def test_null(self):
        data = {
            "title": ""
        }
        response = self.postSampleTrack(sampleFilename="sample.mp3", dataJson=data)
        assert response.status_code == status.HTTP_201_CREATED
        titleKey = AudioMetadataService.METADATA_DICT_KEYS.TITLE
        assert self.savedTrackMetadata[titleKey] in ["", None]
