#!/usr/bin/env python

from rest_framework import status
from bodzify_api import settings
from bodzify_api.serializer.playlist.children.simple.input.schema.SimplePlaylistSaveSchemaSerializer import FIELDS
from bodzify_api.test.view.playlist.children.simple.SimplePlaylistTestCase import SimplePlaylistTestCase


class TestCase(SimplePlaylistTestCase):

    def test_longest(self):
        data = {FIELDS.NAME: "a" * settings.SIMPLE_PLAYLIST_NAME_LENGTH_MAX}
        response = self.post_simple_playlist(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore

    def test_error_when_too_long(self):
        data = {FIELDS.NAME: "a" * (settings.SIMPLE_PLAYLIST_NAME_LENGTH_MAX + 1)}
        response = self.post_simple_playlist(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
