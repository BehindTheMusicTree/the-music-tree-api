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
        response = self.post_sample_track(sample_filename="sample.wav", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        title_key = AudioMetadataService.METADATA_DICT_KEYS.TITLE
        assert self.saved_track_metadata[title_key] == title

    def test_null(self):
        data = {
            "title": ""
        }
        response = self.post_sample_track(sample_filename="sample.wav", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        title_key = AudioMetadataService.METADATA_DICT_KEYS.TITLE
        assert self.saved_track_metadata[title_key] in ["", None]
