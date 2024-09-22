#!/usr/bin/env python

import pytest
from rest_framework import status
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.BasePlaylist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_removal_then_next_tracks_in_playlist_decrease_position(self):
        track_old_position_3 = self.model_fixture_factory.create_lib_track(title="We're All To Blame")
        track_old_position_2 = self.model_fixture_factory.create_lib_track(title="Still Waiting")
        track_old_position_1 = self.model_fixture_factory.create_lib_track(title="The Hell Song")

        base_playlist = SimplePlaylist.objects.get(name=PLAYLIST_SPECIAL_NAMES.ALL).base_playlist

        response = self.delete_lib_track(lib_track_uuid=track_old_position_1.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert PlaylistLibTrackRelation.objects.get(
            base_playlist=base_playlist, library_track=track_old_position_2).position == 1
        assert PlaylistLibTrackRelation.objects.get(
            base_playlist=base_playlist, library_track=track_old_position_3).position == 2
