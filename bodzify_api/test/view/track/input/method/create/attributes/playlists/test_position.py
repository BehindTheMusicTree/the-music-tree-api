#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel
from bodzify_api.model.AllLibTrackMixin import AllLibTrackMixin
from bodzify_api.model.playlist.children.ManualPlaylist import ManualPlaylist
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_create_then_in_first_position_of_all_playlist_and_other_tracks_after(self):
        lib_track1 = self.model_fixture_factory.create_lib_track_with_file(title="We're All To Blame")
        lib_track2 = self.model_fixture_factory.create_lib_track_with_file(title="We're All To lol")
        response = self._post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED
        all_tracks_mixin = AllLibTrackMixin.objects.get(user=self.test_user1)
        assert LibTrackPlaylistPositionRel.objects.get(base_playlist=all_tracks_mixin,
                                                       library_track=self.saved_lib_track).position == 1
        assert LibTrackPlaylistPositionRel.objects.get(
            base_playlist=all_tracks_mixin, library_track=lib_track1).position == 3
        assert LibTrackPlaylistPositionRel.objects.get(
            base_playlist=all_tracks_mixin, library_track=lib_track2).position == 2
