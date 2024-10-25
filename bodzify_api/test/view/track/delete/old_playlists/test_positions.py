#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel
from bodzify_api.model.LibTrackMixin import SpecialNames as LibTrackMixinSpecialNames
from bodzify_api.model.playlist.children.ManualPlaylist import ManualPlaylist
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_removal_then_next_tracks_in_playlist_decrease_position(self):
        track_old_position_3 = self.model_fixture_factory.create_lib_track_with_file(title="We're All To Blame")
        track_old_position_2 = self.model_fixture_factory.create_lib_track_with_file(title="Still Waiting")
        track_old_position_1 = self.model_fixture_factory.create_lib_track_with_file(title="The Hell Song")

        base_playlist = ManualPlaylist.objects.get(name=LibTrackMixinSpecialNames.ALL).base_playlist

        response = self._delete_lib_track(lib_track_uuid=track_old_position_1.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibTrackPlaylistPositionRel.objects.get(
            base_playlist=base_playlist, library_track=track_old_position_2).position == 1
        assert LibTrackPlaylistPositionRel.objects.get(
            base_playlist=base_playlist, library_track=track_old_position_3).position == 2
