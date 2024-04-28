#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.playlist.children.simple.SimplePlaylistTestCase import SimplePlaylistTestCase


class TestCase(SimplePlaylistTestCase):

    def test_extra_field_then_error(self):
        simple_playlist = self.model_fixture_factory.create_simple_playlist(name="teuf")
        data = {'nonExistingField': 'oifjqoif'}
        response = self.put_simple_playlist(simple_playlist_uuid=simple_playlist.playlist.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
