#!/usr/bin/env python

import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_removal_then_next_tracks_in_playlist_decrease_position(self):
        track_old_position_3 = G(LibraryTrack, user=self.test_user, title="We're All To Blame")
        track_old_position_2 = G(LibraryTrack, user=self.test_user, title="Still Waiting")
        track_old_position_1 = G(LibraryTrack, user=self.test_user, title="The Hell Song")

        playlist = SimplePlaylist.objects.get(playlist__user=self.test_user, name=PLAYLIST_SPECIAL_NAMES.ALL).playlist

        response = self.delete_lib_track(lib_track_uuid=track_old_position_1.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert PlaylistLibTrackRelation.objects.get(playlist=playlist, library_track=track_old_position_2).position == 1
        assert PlaylistLibTrackRelation.objects.get(playlist=playlist, library_track=track_old_position_3).position == 2
