#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.playlist.children.criteria.input.query_param import Fields as GetQueryParams
from bodzify_api.serializer.schema.playlist.children.criteria.output.detailed import Fields as GetResultFields
from bodzify_api.test.view.playlist.children.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_filter_empty_then_return_genre_without_parent(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Koko", parent=genre_rock)

        response = self._get_genre_playlists(parent='')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1

    def test_get_two_by_parent_none(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        rock_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=rock_genre).base_playlist
        rap_genre = self.model_fixture_factory.create_genre(name="Rap")
        rap_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=rap_genre).base_playlist
        data_dict = {GetQueryParams.PARENT: ""}

        response = self._get_genre_playlists(data_dict=data_dict)

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 3

        results_rock_playlist = \
            [result for result in self.results if result[GetResultFields.UUID] == rock_playlist.uuid]
        assert results_rock_playlist

        results_rap_playlist = \
            [result for result in self.results if result[GetResultFields.UUID] == rap_playlist.uuid]
        assert results_rap_playlist
