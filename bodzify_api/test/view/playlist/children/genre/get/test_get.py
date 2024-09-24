#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.playlist.children.criteria.output.with_tracks \
    import Fields as GET_RESULT_FIELDS
from bodzify_api.serializer.playlist.children.criteria.input.query_param \
    import Fields as GET_QUERY_PARAM
from bodzify_api.test.view.playlist.children.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_get_by_name_of_criteria(self):
        rock_criteria_name = "Rock"
        self.model_fixture_factory.create_genre(name=rock_criteria_name)
        data_dict = {GET_QUERY_PARAM.NAME: rock_criteria_name}
        response = self.get_genre_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][GET_RESULT_FIELDS.NAME] == rock_criteria_name

    def test_get_two_by_parent_none(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        rock_playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).base_playlist
        rap_genre = self.model_fixture_factory.create_genre(name="Rap")
        rap_playlist = CriteriaPlaylist.objects.get(criteria=rap_genre).base_playlist
        data_dict = {GET_QUERY_PARAM.PARENT: ""}
        response = self.get_genre_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 3

        results_rock_playlist = \
            [result for result in self.results if result[GET_RESULT_FIELDS.UUID] == rock_playlist.uuid]
        assert results_rock_playlist

        results_rap_playlist = \
            [result for result in self.results if result[GET_RESULT_FIELDS.UUID] == rap_playlist.uuid]
        assert results_rap_playlist
