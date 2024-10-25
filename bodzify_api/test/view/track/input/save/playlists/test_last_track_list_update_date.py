#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):
    def test_track_newly_linked_to_genre_then_update_genre_playlist_last_track_list_update_date(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        criteria_playlist: CriteriaPlaylist = genre.criteria_playlist
        genre_playlist_last_track_list_update_date_before_update = \
            criteria_playlist.base_playlist.last_track_list_update_date
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        data = {PutFields.GENRE_NAME: genre.name}
        response = self._put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        genre.refresh_from_db()
        criteria_playlist: CriteriaPlaylist = genre.criteria_playlist
        assert criteria_playlist.base_playlist.last_track_list_update_date > \
            genre_playlist_last_track_list_update_date_before_update

    def test_track_newly_linked_to_genre_then_update_genre_parent_playlist_last_track_list_update_date(self):
        genre_parent = self.model_fixture_factory.create_genre(name='rock')
        genre = self.model_fixture_factory.create_genre(name='rock hard', parent=genre_parent)
        criteria_playlist: CriteriaPlaylist = genre.criteria_playlist
        genre_parent_playlist_last_track_list_update_date_before_update = \
            criteria_playlist.base_playlist.last_track_list_update_date
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        data = {PutFields.GENRE_NAME: genre.name}
        response = self._put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        genre_parent.refresh_from_db()

        parent_criteria_playlist: CriteriaPlaylist = genre_parent.criteria_playlist
        assert genre_parent_playlist_last_track_list_update_date_before_update < \
            parent_criteria_playlist.base_playlist.last_track_list_update_date

    def test_track_newly_linked_to_no_genre_then_update_genreless_playlist_last_track_list_update_date(self):
        genreless_base_playlist = CriteriaPlaylist.objects.get(user=self.test_user1,
                                                               type=CriteriaTypesId.GENRE,
                                                               criteria=None).base_playlist
        genreless_base_playlist_last_track_list_update_date_before_update = \
            genreless_base_playlist.last_track_list_update_date

        genre = self.model_fixture_factory.create_genre(name='rock')
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", genre=genre)

        data = {PutFields.GENRE_NAME: ''}
        response = self._put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        genreless_base_playlist.refresh_from_db()
        assert genreless_base_playlist.last_track_list_update_date > \
            genreless_base_playlist_last_track_list_update_date_before_update
