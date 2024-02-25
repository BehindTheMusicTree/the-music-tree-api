#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_not_provided_then_unchanged(self):
        simple_playlist_name = "simple_playlist_name"
        simpe_playlist = G(SimplePlaylist, name=simple_playlist_name)
        response = self.put_simple_playlist(simple_playlist_uuid=simpe_playlist.uuid, data_json={})
        assert response.status_code == status.HTTP_200_OK
        updated_simpe_playlist = SimplePlaylist.objects.get(name=simple_playlist_name)
        assert updated_simpe_playlist.name == simple_playlist_name

    def test_ok(self):
        simpe_playlist = G(SimplePlaylist, name="teuf")
        simple_playlist_name_new = "teuf2"
        data = {
            ATTRIBUTES_LABEL.NAME: simple_playlist_name_new
        }
        response = self.put_simple_playlist(simple_playlist_uuid=simpe_playlist.uuid, data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        updated_simple_playlist = SimplePlaylist.objects.get(uuid=simpe_playlist.uuid)
        assert updated_simple_playlist.name == simple_playlist_name_new
