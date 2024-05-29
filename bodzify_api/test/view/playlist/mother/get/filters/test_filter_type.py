#!/usr/bin/env python

import logging
from rest_framework import status

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist import TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL, \
    SPECIAL_NAMES as CRITERIA_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.SimplePlaylist \
    import SimplePlaylist, SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES, TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL
from bodzify_api.serializer.playlist.base.input.query_param import FIELDS as GET_QUERY_PARAM
from bodzify_api.serializer.playlist.base.output.with_tracks import FIELDS as PLAYLIST_GET_FIELDS
from bodzify_api.test.get_filters.GetFilterWithSpecificValuesTestCase import GetFilterWithSpecificValuesTestCase
from bodzify_api.test.view.playlist.base.PlaylistTestCase import PlaylistTestCase


class TestCase(GetFilterWithSpecificValuesTestCase, PlaylistTestCase):

    def setUp(self, methods_names_to_implement=None):
        specific_values = [
            CRITERIA_PLAYLIST_TYPES_LABEL.GENRE,
            CRITERIA_PLAYLIST_TYPES_LABEL.TAG,
            SIMPLE_PLAYLIST_SPECIAL_NAMES
        ]
        return super().setUp(specific_values=specific_values,
                             allow_empty_value=False,
                             methods_names_to_implement=methods_names_to_implement)

    def test_is_not_provided_then_results(self):
        rock_criteria_name = "Rock"
        self.model_fixture_factory.create_genre(name=rock_criteria_name)

        simple_playlist_name = "Teuf"
        self.model_fixture_factory.create_simple_playlist(name=simple_playlist_name)

        response = self.get_playlists()
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 5
        names = [result[PLAYLIST_GET_FIELDS.NAME] for result in self.results]
        assert rock_criteria_name in names
        assert simple_playlist_name in names
        assert CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS in names
        assert CRITERIA_PLAYLIST_SPECIAL_NAMES.TAGLESS in names
        assert SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL in names

    def test_is_empty_then_error(self):
        data_dict = {GET_QUERY_PARAM.TYPE: ''}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_value_is_genre_then_resultst(self):
        rock_criteria_name = "Rock n roll"
        self.model_fixture_factory.create_genre(name=rock_criteria_name)
        data_dict = {GET_QUERY_PARAM.TYPE: CRITERIA_PLAYLIST_TYPES_LABEL.GENRE}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PLAYLIST_GET_FIELDS.NAME] for result in self.results]
        assert rock_criteria_name in names
        assert CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS in names

    def test_value_is_tag_then_results(self):
        data_dict = {GET_QUERY_PARAM.TYPE: CRITERIA_PLAYLIST_TYPES_LABEL.TAG}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        names = [result[PLAYLIST_GET_FIELDS.NAME] for result in self.results]
        assert CRITERIA_PLAYLIST_SPECIAL_NAMES.TAGLESS in names

    def test_value_is_simple_then_results(self):
        simple_playlist_name = "Teuf"
        self.model_fixture_factory.create_simple_playlist(name=simple_playlist_name)
        self.model_fixture_factory.create_genre(name='rock')

        data_dict = {GET_QUERY_PARAM.TYPE: SIMPLE_PLAYLIST_TYPE_LABEL}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PLAYLIST_GET_FIELDS.NAME] for result in self.results]
        assert SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL in names
        assert simple_playlist_name in names

    def test_value_is_wrong_then_error(self):
        data_dict = {GET_QUERY_PARAM.TYPE: 'wrong_value'}
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
