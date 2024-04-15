#!/usr/bin/env python

import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.endpoint.LibTrackPutSerializer import FIELDS as PUT_FIELDS
from bodzify_api.test.view import criteria
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):
    def test_track_newly_linked_to_genre_then_update_genre_playlist_last_track_list_update_date(self):
        genre = G(Criteria, name='rock', user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        genre_playlist_last_track_list_update_date_before_update = (
            genre.criteria_playlist.playlist.last_track_list_update_date  # type: ignore
        )
        lib_track = G(LibraryTrack, user=self.test_user, title="Love")

        data = {PUT_FIELDS.GENRE_NAME: genre.name}  # type: ignore
        response = self.put_lib_track(lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        genre.refresh_from_db()  # type: ignore
        assert genre.criteria_playlist.playlist.last_track_list_update_date > (  # type: ignore
            genre_playlist_last_track_list_update_date_before_update
        )

    def test_track_newly_linked_to_genre_then_update_genre_parent_playlist_last_track_list_update_date(self):
        genre_parent = G(Criteria, name='rock', user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        genre = G(Criteria, name='rock hard', user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=genre_parent)
        genre_parent_playlist_last_track_list_update_date_before_update = (
            genre_parent.criteria_playlist.playlist.last_track_list_update_date  # type: ignore
        )
        lib_track = G(LibraryTrack, user=self.test_user, title="Love")

        data = {PUT_FIELDS.GENRE_NAME: genre.name}  # type: ignore
        response = self.put_lib_track(lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        genre_parent.refresh_from_db()  # type: ignore
        assert genre_parent.criteria_playlist.playlist.last_track_list_update_date > (  # type: ignore
            genre_parent_playlist_last_track_list_update_date_before_update
        )

    def test_track_newly_linked_to_no_genre_then_update_genreless_playlist_last_track_list_update_date(self):
        genreless_base_playlist = CriteriaPlaylist.objects.get(playlist__user=self.test_user,
                                                               type=CRITERIA_TYPES_ID.GENRE,
                                                               criteria=None).playlist
        genreless_base_playlist_last_track_list_update_date_before_update = (
            genreless_base_playlist.last_track_list_update_date  # type: ignore
        )

        genre = G(Criteria, name='rock', user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        lib_track = G(LibraryTrack, user=self.test_user, title="Love", genre=genre)

        data = {PUT_FIELDS.GENRE_NAME: ''}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        genreless_base_playlist.refresh_from_db()  # type: ignore
        assert genreless_base_playlist.last_track_list_update_date > (  # type: ignore
            genreless_base_playlist_last_track_list_update_date_before_update
        )
