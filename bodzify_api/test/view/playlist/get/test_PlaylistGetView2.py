#!/usr/bin/env python
import pprint
from bodzify_api.test.view.playlist.PlaylistViewTestCase import PlaylistViewTestCase
from bodzify_api.model.playlist.Playlist import Playlist


class PlaylistGetViewTestCase1(PlaylistViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewPlaylistGetData2']

    """
    When a playlist is a linked to the "Rock" criteria and doesn't have a custom name, the name of
    the playlist is the name of the criteria.
    """
    def test_playlistGet1(self):
        self._login(self.testUser)
        response = self.get(
                playlistUuid=Playlist.objects.get(user=self.testUser, criteria__name="Rock").uuid)
        assert response.json()['name'] == "Rock"
