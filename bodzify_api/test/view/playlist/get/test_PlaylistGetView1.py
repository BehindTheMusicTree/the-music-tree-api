#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.playlist.PlaylistViewTestCase import PlaylistViewTestCase
from bodzify_api.model.playlist.Playlist import Playlist


class PlaylistGetViewTestCase1(PlaylistViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewPlaylistGetData1']

    """
    When a criteria playlist "Hard rock" has a custom name "Daddy's rock", it must be displayed 
    instead of the name of the criteria.
    """
    def test_playlistGet1(self):
        self._login(self.testUser)
        response = self.get(playlistUuid=Playlist.objects.get(
                user=self.testUser, customName="Daddy's rock").uuid)
        assert response.json()['name'] == "Daddy's rock"
