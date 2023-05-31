#!/usr/bin/env python

from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.playlist.SimplePlaylist import \
    ATTRIBUTES_LABEL as SIMPLE_PLAYLIST_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):
    
    def test_longestCustomName(self):
        data = {
            SIMPLE_PLAYLIST_ATTRIBUTES_LABEL.CUSTOM_NAME: "a" * settings.CRITERIA_NAME_MAX_CHAR
        }
        response = self.post