#!/usr/bin/env python

import pytest
from rest_framework import status
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
        genre = self.model_fixture_factory.create_genre(name='rock')
        genre_playlist_last_track_list_update_date_before_update = (
            genre.criteria_playlist.playlist.last_track_list_update_date  # type: ignore
        )
        lib_track = self.model_fixture_factory.create_lib_track(title="Love")

        data = {PUT_FIELDS.GENRE_NAME: genre.name}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        genre.refresh_from_db()
        assert genre.criteria_playlist.playlist.last_track_list_update_date > (  # type: ignore
            genre_playlist_last_track_list_update_date_before_update
        )

    def test_track_newly_linked_to_genre_then_update_genre_parent_playlist_last_track_list_update_date(self):
        genre_parent = self.model_fixture_factory.create_genre(name='rock')
        genre = self.model_fixture_factory.create_genre(name='rock hard', parent=genre_parent)
        genre_parent_playlist_last_track_list_update_date_before_update = \
            genre_parent.criteria_playlist.playlist.last_track_list_update_date  # type: ignore
        lib_track = self.model_fixture_factory.create_lib_track(title="Love")

        data = {PUT_FIELDS.GENRE_NAME: genre.name}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        genre_parent.refresh_from_db()
        assert genre_parent_playlist_last_track_list_update_date_before_update < \
            genre_parent.criteria_playlist.playlist.last_track_list_update_date  # type: ignore

    def test_track_newly_linked_to_no_genre_then_update_genreless_playlist_last_track_list_update_date(self):
        genreless_parent_playlist = CriteriaPlaylist.objects.get(type=CRITERIA_TYPES_ID.GENRE, criteria=None).playlist
        genreless_parent_playlist_last_track_list_update_date_before_update = \
            genreless_parent_playlist.last_track_list_update_date

        genre = self.model_fixture_factory.create_genre(name='rock')
        lib_track = self.model_fixture_factory.create_lib_track(title="Love", genre=genre)

        data = {PUT_FIELDS.GENRE_NAME: ''}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        genreless_parent_playlist.refresh_from_db()
        assert genreless_parent_playlist.last_track_list_update_date > \
            genreless_parent_playlist_last_track_list_update_date_before_update
