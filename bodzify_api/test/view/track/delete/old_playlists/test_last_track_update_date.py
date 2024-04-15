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

    def test_delete_then_update_the_all_playlist_last_track_update_date(self):
        track = G(LibraryTrack, user=self.test_user, title="We're All To Blame")
        all_playlist = SimplePlaylist.objects.get(playlist__user=self.test_user,
                                                  name=PLAYLIST_SPECIAL_NAMES.ALL).playlist
        last_track_list_update_date_before_deletion = all_playlist.last_track_list_update_date
        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        all_playlist.refresh_from_db()
        assert all_playlist.last_track_list_update_date > last_track_list_update_date_before_deletion  # type: ignore

    def test_delete_then_update_genre_playlist_last_track_update_date(self):
        genre = G(Criteria, name='rock', user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        genre_playlist = genre.criteria_playlist.playlist  # type: ignore
        track = G(LibraryTrack, user=self.test_user, title="We're All To Blame", genre=genre)
        genre_playlist_last_track_list_update_date_before_deletion = (
            genre_playlist.last_track_list_update_date  # type: ignore
        )
        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        genre_playlist.refresh_from_db()
        assert genre_playlist.last_track_list_update_date > genre_playlist_last_track_list_update_date_before_deletion  # type: ignore

    def test_delete_then_update_parent_of_parent_of_genre_playlist_last_track_update_date(self):
        genre1 = G(Criteria, name='rock', user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        genre2 = G(Criteria, name='ff', user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=genre1)
        genre3 = G(Criteria, name='fffffffd', user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=genre2)

        genre1_playlist = genre1.criteria_playlist.playlist  # type: ignore
        track = G(LibraryTrack, user=self.test_user, title="We're All To Blame", genre=genre3)
        genre1_playlist_last_track_list_update_date_before_deletion = (
            genre1_playlist.last_track_list_update_date  # type: ignore
        )
        response = self.delete_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        genre1_playlist.refresh_from_db()
        assert genre1_playlist.last_track_list_update_date > genre1_playlist_last_track_list_update_date_before_deletion  # type: ignore
