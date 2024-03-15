#!/usr/bin/env python

import logging
from rest_framework import status
from ddf import G

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID, CRITERIA_TYPES_LABEL
from bodzify_api.model.playlist.children.CriteriaPlaylist import TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL, \
    SPECIAL_NAMES as CRITERIA_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.SimplePlaylist \
    import SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES, TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL, SimplePlaylist
from bodzify_api.serializer.playlist.mother.input.PlaylistQueryParamSerializer import FIELDS as GET_QUERY_PARAM
from bodzify_api.serializer.playlist.mother.output.PlaylistWithTracksSerializer import FIELDS as PLAYLIST_GET_FIELDS
from bodzify_api.test.ApiTestCase import ApiViewTestCase
from bodzify_api.test.view.playlist.children import genre

logger = logging.getLogger('bodyzify_api')


class TestCase(ApiViewTestCase):

    def test_type_genre_and_name_tagless_then_no_result(self):
        data_dict = {
            GET_QUERY_PARAM.TYPE: CRITERIA_PLAYLIST_TYPES_LABEL.GENRE,
            GET_QUERY_PARAM.NAME: CRITERIA_PLAYLIST_SPECIAL_NAMES.TAGLESS
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert len(self.results) == 0

    def test_type_genre_and_name_genreless_then_one_result(self):
        data_dict = {
            GET_QUERY_PARAM.TYPE: CRITERIA_PLAYLIST_TYPES_LABEL.GENRE,
            GET_QUERY_PARAM.NAME: CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert len(self.results) == 1
        assert self.results[0][PLAYLIST_GET_FIELDS.NAME] == CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS

    def test_type_simple_and_name_all_then_one_result(self):
        data_dict = {
            GET_QUERY_PARAM.TYPE: SIMPLE_PLAYLIST_TYPE_LABEL,
            GET_QUERY_PARAM.NAME: SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert len(self.results) == 1
        assert self.results[0][PLAYLIST_GET_FIELDS.NAME] == SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL

    def test_type_genre_and_genre_name_then_results(self):
        genre1_name = "Rock"
        G(Criteria, user=self.test_user, name=genre1_name, type=CRITERIA_TYPES_ID.GENRE)
        genre2_name = "Punk rock"
        G(Criteria, user=self.test_user, name=genre2_name, type=CRITERIA_TYPES_ID.GENRE)

        data_dict = {
            GET_QUERY_PARAM.TYPE: CRITERIA_TYPES_LABEL.GENRE,
            GET_QUERY_PARAM.NAME: 'rock'
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert len(self.results) == 2
        names = [result[PLAYLIST_GET_FIELDS.NAME] for result in self.results]
        assert genre1_name in names
        assert genre2_name in names

    def test_type_simple_and_name_contains_all_then_results(self):
        gsimple_playlist_name = "allez laaaa"
        G(SimplePlaylist, playlist__user=self.test_user, name=gsimple_playlist_name)

        data_dict = {
            GET_QUERY_PARAM.TYPE: SIMPLE_PLAYLIST_TYPE_LABEL,
            GET_QUERY_PARAM.NAME: 'all'
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert len(self.results) == 2
        names = [result[PLAYLIST_GET_FIELDS.NAME] for result in self.results]
        assert gsimple_playlist_name in names
        assert SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL in names
