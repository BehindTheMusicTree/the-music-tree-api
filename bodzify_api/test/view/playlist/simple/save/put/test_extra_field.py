#!/usr/bin/env python
from importlib import simple
from rest_framework import status
from ddf import G
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_error(self):
        simple_playlist = G(SimplePlaylist, 
                  user=self.test_user,
                  name="simple_playlist_name")
        data = {
            'nonExistingField': 'oifjqoif'
        }
        response = self.put(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST