#!/usr/bin/env python

import pytest
from rest_framework import status
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.playlist.BasePlaylist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_create_then_in_first_position_of_all_playlist_and_other_tracks_after(self):
        lib_track1 = self.model_fixture_factory.create_lib_track(title="We're All To Blame")
        lib_track2 = self.model_fixture_factory.create_lib_track(title="We're All To lol")
        response = self.post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED
        all_playlist = SimplePlaylist.objects.get(name=PLAYLIST_SPECIAL_NAMES.ALL).base_playlist
        assert PlaylistLibTrackRelation.objects.get(base_playlist=all_playlist,
                                                    library_track=self.saved_lib_track).position == 1
        assert PlaylistLibTrackRelation.objects.get(base_playlist=all_playlist, library_track=lib_track1).position == 3
        assert PlaylistLibTrackRelation.objects.get(base_playlist=all_playlist, library_track=lib_track2).position == 2
