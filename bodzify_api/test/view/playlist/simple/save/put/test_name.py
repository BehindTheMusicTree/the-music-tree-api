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
        simple_playlist_name = "simple_playlist_name"
        simpe_playlist = G(SimplePlaylist, name=simple_playlist_name, playlist__user=self.test_user)
        logger.debug(f"simpe_playlist: {simpe_playlist}")
        logger.debug(f"simpe_playlist: {simpe_playlist.playlist.uuid}")
        response = self.put_simple_playlist(simple_playlist_uuid=simpe_playlist.playlist.uuid, data_json={})
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        updated_simpe_playlist = SimplePlaylist.objects.get(name=simple_playlist_name)
        assert updated_simpe_playlist.name == simple_playlist_name

    def test_ok(self):
        simpe_playlist = G(SimplePlaylist, name="teuf")
        simple_playlist_name_new = "teuf2"
        data = {
            PLAYLIST_ATTRIBUTES_LABEL.NAME: simple_playlist_name_new
        }
        response = self.put_simple_playlist(simple_playlist_uuid=simpe_playlist.uuid, data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        updated_simple_playlist = SimplePlaylist.objects.get(uuid=simpe_playlist.uuid)
        assert updated_simple_playlist.name == simple_playlist_name_new
