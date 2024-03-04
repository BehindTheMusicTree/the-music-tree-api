#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_error(self):
        simple_playlist = G(SimplePlaylist,
                            playlist__user=self.test_user,
                            name="teuf")
        data = {
            'nonExistingField': 'oifjqoif'
        }
        response = self.put_simple_playlist(
            simple_playlist_uuid=simple_playlist.playlist.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
