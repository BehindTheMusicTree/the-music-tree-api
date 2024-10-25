#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import \
    ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_extra_field_then_error(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name="teuf")
        data = {'nonExistingField': 'oifjqoif'}
        response = self.put_manual_playlist(manual_playlist_uuid=manual_playlist.base_playlist.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
