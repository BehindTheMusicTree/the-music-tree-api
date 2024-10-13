#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel
from bodzify_api.model.playlist.BasePlaylist import \
    SpecialNames as PlaylistSpecialNames
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_create_then_in_first_position_of_all_playlist_and_other_tracks_after(self):
        lib_track1 = self.model_fixture_factory.create_lib_track(title="We're All To Blame")
        lib_track2 = self.model_fixture_factory.create_lib_track(title="We're All To lol")
        response = self.post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED
        playlist_all = SimplePlaylist.objects.get(name=PlaylistSpecialNames.ALL).base_playlist
        assert LibTrackPlaylistPositionRel.objects.get(base_playlist=playlist_all,
                                                       library_track=self.lib_track_saved).position == 1
        assert LibTrackPlaylistPositionRel.objects.get(
            base_playlist=playlist_all, library_track=lib_track1).position == 3
        assert LibTrackPlaylistPositionRel.objects.get(
            base_playlist=playlist_all, library_track=lib_track2).position == 2
