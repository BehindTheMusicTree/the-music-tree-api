#!/usr/bin/env python

import logging
from rest_framework import status
from ddf import G
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.test.view.playlist.children.simple.SimplePlaylistTestCase import SimplePlaylistTestCase

logger = logging.getLogger('bodzify_api')


class TestCase(SimplePlaylistTestCase):

    def test_value_then_ok(self):
        simpe_playlist = G(SimplePlaylist, playlist__user=self.test_user, name="teuf")
        simple_playlist_name_new = "teuf2"
        data = {PLAYLIST_ATTRIBUTES_LABEL.NAME: simple_playlist_name_new}
        response = self.put_simple_playlist(
            simple_playlist_uuid=simpe_playlist.playlist.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_simple_playlist.name == simple_playlist_name_new

    def test_not_provided_then_unchanged(self):
        simple_playlist_name = "cuisine"
        simpe_playlist = G(SimplePlaylist, name=simple_playlist_name, playlist__user=self.test_user)
        response = self.put_simple_playlist(
            simple_playlist_uuid=simpe_playlist.playlist.uuid, data_dict={})  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_simple_playlist.name == simple_playlist_name

    def test_empty_then_error(self):
        simple_playlist_uuid = G(SimplePlaylist, name='foero', playlist__user=self.test_user).uuid  # type: ignore
        data = {PLAYLIST_ATTRIBUTES_LABEL.NAME: ""}
        response = self.put_simple_playlist(simple_playlist_uuid=simple_playlist_uuid.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
