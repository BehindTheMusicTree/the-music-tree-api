#!/usr/bin/env python

import logging
from rest_framework import status

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.children.SimplePlaylist \
    import SimplePlaylist, SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.CriteriaPlaylist import SPECIAL_NAMES as CRITERIA_PLAYLIST_SPECIAL_NAMES
from bodzify_api.serializer.playlist.base.input.query_param import FIELDS as GET_QUERY_PARAM
from bodzify_api.test.get_filters.GetFilterWithFreeValuesTestCase import GetFilterWithFreeValuesTestCase
from bodzify_api.test.view.playlist.base.PlaylistTestCase import PlaylistTestCase


class TestCase(GetFilterWithFreeValuesTestCase, PlaylistTestCase):

    def setUp(self, methods_names_to_implement=None):
        return super().setUp(allow_empty_value=False, methods_names_to_implement=methods_names_to_implement)

    def test_is_empty_then_error(self):
        data_dict = {GET_QUERY_PARAM.NAME: ''}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_is_not_provided_then_results(self):
        rock_criteria_name = "Rock"
        self.model_fixture_factory.create_genre(name=rock_criteria_name)

        simple_playlist_name = "Teuf"
        self.model_fixture_factory.create_simple_playlist(name=simple_playlist_name)

        response = self.get_playlists()
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == BasePlaylist.objects.filter(user=self.test_user.django_user).count()

    def test_different_case_then_results(self):
        simple_playlist_name = "Teuf"
        self.model_fixture_factory.create_simple_playlist(name=simple_playlist_name)

        data_dict = {GET_QUERY_PARAM.NAME: simple_playlist_name.upper()}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        names_lowered = [result[GET_QUERY_PARAM.NAME].lower() for result in self.results]
        assert simple_playlist_name.lower() in names_lowered

    def test_genreless_special_name_then_results(self):
        data_dict = {GET_QUERY_PARAM.NAME: 'geNr'}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][GET_QUERY_PARAM.NAME] == CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS

    def test_tagless_special_name_then_results(self):
        data_dict = {GET_QUERY_PARAM.NAME: 'aGl'}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][GET_QUERY_PARAM.NAME] == CRITERIA_PLAYLIST_SPECIAL_NAMES.TAGLESS

    def test_all_special_name_then_results(self):
        data_dict = {GET_QUERY_PARAM.NAME: 'Al'}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][GET_QUERY_PARAM.NAME] == SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL

    def test_value_in_simple_criteria_and_special_names_then_results(self):
        simple_playlist_name = "lEsson"
        self.model_fixture_factory.create_simple_playlist(name=simple_playlist_name)
        criteria_name = "leSsa"
        self.model_fixture_factory.create_genre(name=criteria_name)

        data_dict = {GET_QUERY_PARAM.NAME: 'Less'}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 4
        names_lowered = [result[GET_QUERY_PARAM.NAME].lower() for result in self.results]
        assert simple_playlist_name.lower() in names_lowered
        assert criteria_name.lower() in names_lowered
        assert CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS.lower() in names_lowered
        assert CRITERIA_PLAYLIST_SPECIAL_NAMES.TAGLESS.lower() in names_lowered
