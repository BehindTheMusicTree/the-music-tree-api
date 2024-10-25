#!/usr/bin/env python

from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.playlist.children.simple.input.schema import Fields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_multiple_values_then_error(self):
        data = {Fields.NAME: ["value", "value2"]}
        response = self.post_manual_playlist(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_longest(self):
        data = {Fields.NAME: "a" * settings.MANUAL_PLAYLIST_NAME_LEN_MAX}
        response = self.post_manual_playlist(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_error_when_too_long(self):
        data = {Fields.NAME: "a" * (settings.MANUAL_PLAYLIST_NAME_LEN_MAX + 1)}
        response = self.post_manual_playlist(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def text_already_exists_then_error(self):
        data = {Fields.NAME: "value"}
        response = self.post_manual_playlist(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        response = self.post_manual_playlist(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
