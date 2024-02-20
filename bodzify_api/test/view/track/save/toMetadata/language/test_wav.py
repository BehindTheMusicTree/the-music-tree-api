#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_longest(self):
        language = "a" * settings.TRACK_LANGUAGE_LENGTH_MAX
        data = {
            TRACK_ATTRIBUTES_LABEL.LANGUAGE: language
        }
        response = self.post_sample_track(sample_filename="sample.wav", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        languageKey = AudioMetadataManager.METADATA_DICT_KEYS.LANGUAGE
        assert self.saved_track_metadata[languageKey] == language

    def test_null(self):
        data = {
            TRACK_ATTRIBUTES_LABEL.LANGUAGE: ""
        }
        response = self.post_sample_track(sample_filename="sample.wav", data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        languageKey = AudioMetadataManager.METADATA_DICT_KEYS.LANGUAGE
        assert self.saved_track_metadata[languageKey] in ["", None]
