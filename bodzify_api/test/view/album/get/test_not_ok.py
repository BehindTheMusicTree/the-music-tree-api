#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase


class TestCase(AlbumTestCase):

    def test_filter_not_existing_then_error(self):
        response = self._get_albums(invalid_filter='test')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
