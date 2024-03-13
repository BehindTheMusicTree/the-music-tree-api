#!/usr/bin/env python

from importlib import simple
from rest_framework import status
from ddf import G

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.CriteriaPlaylist import TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL, \
    SPECIAL_NAMES as CRITERIA_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.serializer.playlist.mother.input.PlaylistQueryParamSerializer import FIELDS as GET_QUERY_FIELDS
from bodzify_api.serializer.playlist.mother.output.PlaylistWithTracksSerializer import FIELDS as GET_RESULT_FIELDS


class TestCase(ApiViewTestCase):

    def test_filter_type_is_none_then_one_genre_playlist_and_one_simple_and_all_and_genreless(self):
        rock_criteria_name = "Rock"
        G(Criteria, user=self.test_user, name=rock_criteria_name, type=CRITERIA_TYPES_ID.GENRE)

        simple_playlist_name = "Teuf"
        G(SimplePlaylist, user=self.test_user, name=simple_playlist_name)

        data_dict = {
            GET_QUERY_FIELDS.NAME: None
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert len(self.results) == 4
        names = [result[GET_RESULT_FIELDS.NAME] for result in self.results]
        assert rock_criteria_name in names
        assert CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS in names

    def test_filter_type_is_genre_then_one_genre_playlist_and_genreless_playlist(self):
        rock_criteria_name = "Rock"
        G(Criteria, user=self.test_user, name=rock_criteria_name, type=CRITERIA_TYPES_ID.GENRE)
        data_dict = {
            GET_QUERY_FIELDS.NAME: CRITERIA_PLAYLIST_TYPES_LABEL.GENRE
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert len(self.results) == 2
        names = [result[GET_RESULT_FIELDS.NAME] for result in self.results]
        assert rock_criteria_name in names
        assert CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS in names
