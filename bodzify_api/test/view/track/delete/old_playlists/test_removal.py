#!/usr/bin/env python

import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_delete_then_remove_from_the_all_playlist(self):
        track = G(LibraryTrack, user=self.test_user, title="We're All To Blame")
        all_playlist = SimplePlaylist.objects.get(playlist__user=self.test_user,
                                                  name=PLAYLIST_SPECIAL_NAMES.ALL).playlist
        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert track not in all_playlist.library_tracks.all()  # type: ignore

    def test_delete_then_remove_from_the_genre_playlists(self):
        genre1_name = "Rock"
        genre1 = G(Criteria, name=genre1_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        genre2_name = "Hard rock"
        genre2 = G(Criteria, name=genre2_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=genre1)
        genre3_name = "Emo"
        genre3 = G(Criteria,
                   name=genre3_name,
                   user=self.test_user,
                   type=CRITERIA_TYPES_ID.GENRE,
                   parent=genre2)

        track = G(LibraryTrack, user=self.test_user, title="Love", genre=genre3)

        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore

        assert track not in genre1.criteria_playlist.playlist.library_tracks.all()  # type: ignore
        assert track not in genre2.criteria_playlist.playlist.library_tracks.all()  # type: ignore
        assert track not in genre3.criteria_playlist.playlist.library_tracks.all()  # type: ignore
