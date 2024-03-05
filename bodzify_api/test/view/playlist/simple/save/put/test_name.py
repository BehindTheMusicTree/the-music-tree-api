#!/usr/bin/env python

import logging
from rest_framework import status
from ddf import G
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL

logger = logging.getLogger('bodzify_api')


class TestCase(ApiViewTestCase):

    def test_not_provided_then_unchanged(self):
        simple_playlist_name = "cuisine"
        simpe_playlist = G(SimplePlaylist, name=simple_playlist_name, playlist__user=self.test_user)
        response = self.put_simple_playlist(
            simple_playlist_uuid=simpe_playlist.playlist.uuid, data_json={})  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        updated_simpe_playlist = SimplePlaylist.objects.get(name=simple_playlist_name)
        assert self.saved_simple_playlist.name == simple_playlist_name

    def test_ok(self):
        simpe_playlist = G(SimplePlaylist, playlist__user=self.test_user, name="teuf")
        simple_playlist_name_new = "teuf2"
        data = {
            PLAYLIST_ATTRIBUTES_LABEL.NAME: simple_playlist_name_new
        }
        response = self.put_simple_playlist(
            simple_playlist_uuid=simpe_playlist.playlist.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_simple_playlist.name == simple_playlist_name_new
