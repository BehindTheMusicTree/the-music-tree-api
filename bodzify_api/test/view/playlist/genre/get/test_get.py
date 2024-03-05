#!/usr/bin/env python

from unittest import result
from rest_framework import status
from ddf import G

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithTracksSerializer \
    import FIELDS as GET_RESULT_FIELDS
from bodzify_api.view.viewset.model.playlist.GenrePlaylistViewSet import GET_QUERY_FIELDS
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_get_by_name_of_criteria(self):
        rock_criteria_name = "Rock"
        rock_genre = G(Criteria,
                       user=self.test_user,
                       name=rock_criteria_name,
                       type=CRITERIA_TYPES_ID.GENRE)
        data_json = {
            GET_QUERY_FIELDS.NAME: rock_criteria_name
        }
        response = self.get_genre_playlists(data_json=data_json)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        results = response.json()[ApiViewTestCase.RESPONSE_FIELDS.RESULTS]  # type: ignore
        assert len(results) == 1
        assert results[0][GET_RESULT_FIELDS.NAME] == rock_criteria_name

    def test_get_two_by_parent_none(self):
        rock_genre = G(Criteria,
                       user=self.test_user,
                       name="Rock",
                       type=CRITERIA_TYPES_ID.GENRE)
        rock_playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist
        rap_genre = G(Criteria,
                      user=self.test_user,
                      name="Rap",
                      type=CRITERIA_TYPES_ID.GENRE)
        rap_playlist = CriteriaPlaylist.objects.get(criteria=rap_genre).playlist

        data_json = {
            GET_QUERY_FIELDS.PARENT: ""
        }
        response = self.get_genre_playlists(data_json=data_json)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        results = response.json()[ApiViewTestCase.RESPONSE_FIELDS.RESULTS]  # type: ignore
        assert len(results) == 2

        results_rock_playlist = [result for result in results if result[GET_RESULT_FIELDS.UUID] == rock_playlist.uuid]
        assert results_rock_playlist

        results_rap_playlist = [result for result in results if result[GET_RESULT_FIELDS.UUID] == rap_playlist.uuid]
        assert results_rap_playlist
