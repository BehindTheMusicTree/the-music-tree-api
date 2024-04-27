#!/usr/bin/env python

import logging
from rest_framework import status
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.test.view.playlist.children.simple.SimplePlaylistTestCase import SimplePlaylistTestCase


class TestCase(SimplePlaylistTestCase):

    def test_value_then_ok(self):
        simpe_playlist = self.model_fixture_factory.create_simple_playlist(name="teuf")
        simple_playlist_name_new = "teuf2"
        data = {PLAYLIST_ATTRIBUTES_LABEL.NAME: simple_playlist_name_new}
        response = self.put_simple_playlist(
            simple_playlist_uuid=simpe_playlist.playlist.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_simple_playlist.name == simple_playlist_name_new

    def test_not_provided_then_unchanged(self):
        simple_playlist_name = "cuisine"
        simpe_playlist = self.model_fixture_factory.create_simple_playlist(name=simple_playlist_name)
        response = self.put_simple_playlist(simple_playlist_uuid=simpe_playlist.playlist.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_simple_playlist.name == simple_playlist_name

    def test_empty_then_error(self):
        uuid = self.model_fixture_factory.create_simple_playlist(name='foero').playlist.uuid
        data = {PLAYLIST_ATTRIBUTES_LABEL.NAME: ""}
        response = self.put_simple_playlist(simple_playlist_uuid=uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
