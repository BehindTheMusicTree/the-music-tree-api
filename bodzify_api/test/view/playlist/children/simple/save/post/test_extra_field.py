#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.playlist.children.simple.SimplePlaylistTestCase import SimplePlaylistTestCase


class TestCase(SimplePlaylistTestCase):

    def test_extra_field_then_error(self):
        data = {'nonExistingField': 'oifjqoif'}
        response = self.post_simple_playlist(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
