#!/usr/bin/env python

from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.playlist.Playlist import \
    ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL

class TestCase(ApiViewTestCase):
    
    def test_longest_custom_name(self):
        data = {
            PLAYLIST_ATTRIBUTES_LABEL.NAME: "a" * settings.PLAYLIST_NAME_MAX_CHAR
        }
        response = self.post_simple_playlist(data)
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_error_when_too_long(self):
        data = {
            PLAYLIST_ATTRIBUTES_LABEL.NAME: "a" * (settings.PLAYLIST_NAME_MAX_CHAR + 1)
        }
        response = self.post_simple_playlist(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST