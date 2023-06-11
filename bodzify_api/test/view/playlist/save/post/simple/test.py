#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.playlist.Playlist import \
    ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):
    
    def test_longestCustomName(self):
        data = {
            PLAYLIST_ATTRIBUTES_LABEL.NAME: "a" * settings.CRITERIA_NAME_MAX_CHAR
        }
        response = self.postSimplePlaylist(data)
        assert response.status_code == status.HTTP_201_CREATED