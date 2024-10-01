#!/usr/bin/env python

import logging
from rest_framework import status

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.children.SimplePlaylist \
    import SimplePlaylist, SpecialNames as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.CriteriaPlaylist import SpecialNames as CriteriaPlaylistSpecialNames
from bodzify_api.serializer.playlist.base.input.query_param import Fields as GetQueryParams
from bodzify_api.test.get_filters.GetFilterWithFreeValuesTestCase import GetFilterWithFreeValuesTestCase
from bodzify_api.test.view.playlist.base.BasePlaylistTestCase import BasePlaylistTestCase


class TestCase(GetFilterWithFreeValuesTestCase, BasePlaylistTestCase):

    def setUp(self, methods_names_to_implement=None):
        return super().setUp(allow_empty_value=False, methods_names_to_implement=methods_names_to_implement)

    def test_is_empty_then_error(self):
        data_dict = {GetQueryParams.NAME: ''}
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

        data_dict = {GetQueryParams.NAME: simple_playlist_name.upper()}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        names_lowered = [result[GetQueryParams.NAME].lower() for result in self.results]
        assert simple_playlist_name.lower() in names_lowered

    def test_genreless_special_name_then_results(self):
        data_dict = {GetQueryParams.NAME: 'geNr'}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][GetQueryParams.NAME] == CriteriaPlaylistSpecialNames.GENRELESS

    def test_tagless_special_name_then_results(self):
        data_dict = {GetQueryParams.NAME: 'aGl'}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][GetQueryParams.NAME] == CriteriaPlaylistSpecialNames.TAGLESS

    def test_all_special_name_then_results(self):
        data_dict = {GetQueryParams.NAME: 'Al'}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][GetQueryParams.NAME] == SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL

    def test_value_in_simple_criteria_and_special_names_then_results(self):
        simple_playlist_name = "lEsson"
        self.model_fixture_factory.create_simple_playlist(name=simple_playlist_name)
        criteria_name = "leSsa"
        self.model_fixture_factory.create_genre(name=criteria_name)

        data_dict = {GetQueryParams.NAME: 'Less'}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 4
        names_lowered = [result[GetQueryParams.NAME].lower() for result in self.results]
        assert simple_playlist_name.lower() in names_lowered
        assert criteria_name.lower() in names_lowered
        assert CriteriaPlaylistSpecialNames.GENRELESS.lower() in names_lowered
        assert CriteriaPlaylistSpecialNames.TAGLESS.lower() in names_lowered
