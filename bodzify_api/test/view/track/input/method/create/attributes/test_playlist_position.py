#!/usr/bin/env python

import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.PlaylistLibraryTrack import PlaylistLibraryTrackRelation
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_create_then_in_last_position_of_all_playlist(self):
        G(LibraryTrack, user=self.test_user, title="We're All To Blame")
        G(LibraryTrack, user=self.test_user, title="We're All To lol")
        response = self.post_lib_track_with_generic_sample_no_tags()  # type: ignore
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        all_playlist = SimplePlaylist.objects.get(name=PLAYLIST_SPECIAL_NAMES.ALL).playlist
        assert PlaylistLibraryTrackRelation.objects.get(playlist=all_playlist,
                                                        library_track=self.saved_lib_track).position == 3
