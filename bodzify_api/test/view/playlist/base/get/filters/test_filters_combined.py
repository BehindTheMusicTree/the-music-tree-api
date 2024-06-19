#!/usr/bin/env python

import logging
from rest_framework import status

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID, CRITERIA_TYPES_LABEL
from bodzify_api.model.playlist.children.CriteriaPlaylist import TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL, \
    SPECIAL_NAMES as CRITERIA_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.SimplePlaylist \
    import SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES, TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL, SimplePlaylist
from bodzify_api.serializer.playlist.base.input.query_param import FIELDS as GET_QUERY_PARAM
from bodzify_api.serializer.playlist.base.output.with_tracks import FIELDS as PLAYLIST_GET_FIELDS
from bodzify_api.test.view.playlist.base.BasePlaylistTestCase import BasePlaylistTestCase


class TestCase(BasePlaylistTestCase):

    def test_type_genre_and_name_tagless_then_no_result(self):
        data_dict = {
            GET_QUERY_PARAM.TYPE: CRITERIA_PLAYLIST_TYPES_LABEL.GENRE,
            GET_QUERY_PARAM.NAME: CRITERIA_PLAYLIST_SPECIAL_NAMES.TAGLESS
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 0

    def test_type_genre_and_name_genreless_then_one_result(self):
        data_dict = {
            GET_QUERY_PARAM.TYPE: CRITERIA_PLAYLIST_TYPES_LABEL.GENRE,
            GET_QUERY_PARAM.NAME: CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][PLAYLIST_GET_FIELDS.NAME] == CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS

    def test_type_simple_and_name_all_then_one_result(self):
        data_dict = {
            GET_QUERY_PARAM.TYPE: SIMPLE_PLAYLIST_TYPE_LABEL,
            GET_QUERY_PARAM.NAME: SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][PLAYLIST_GET_FIELDS.NAME] == SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL

    def test_type_genre_and_genre_name_then_results(self):
        genre1_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre1_name)
        genre2_name = "Punk rock"
        self.model_fixture_factory.create_genre(name=genre2_name)

        data_dict = {
            GET_QUERY_PARAM.TYPE: CRITERIA_TYPES_LABEL.GENRE,
            GET_QUERY_PARAM.NAME: 'rock'
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PLAYLIST_GET_FIELDS.NAME] for result in self.results]
        assert genre1_name in names
        assert genre2_name in names

    def test_type_simple_and_name_contains_all_then_results(self):
        gsimple_playlist_name = "allez laaaa"
        self.model_fixture_factory.create_simple_playlist(name=gsimple_playlist_name)

        data_dict = {
            GET_QUERY_PARAM.TYPE: SIMPLE_PLAYLIST_TYPE_LABEL,
            GET_QUERY_PARAM.NAME: 'all'
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PLAYLIST_GET_FIELDS.NAME] for result in self.results]
        assert gsimple_playlist_name in names
        assert SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL in names
