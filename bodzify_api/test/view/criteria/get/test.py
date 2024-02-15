#!/usr/bin/env python

from ddf import G
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.test.view.ApiViewTestCase import RESPONSE_KEYS, ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as Criteria

class TestCase(ApiViewTestCase):

    def test(self):
        genre_name = "Rock"
        genre = G(Criteria,
                      name=genre_name,
                      user=self.test_user,
                      type=CriteriaTypesId.GENRE)
        response = self.get_genres()
        genre_json_list = response.json()[RESPONSE_KEYS.RESULTS]
        assert len(genre_json_list) == 1
        rock_genre_json = genre_json_list[0]
        assert rock_genre_json[Criteria.NAME] == genre_name
        assert rock_genre_json[Criteria.TYPE] == CriteriaTypesId.GENRE

    def test_two(self):
        G(Criteria,
            name="rock",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        G(Criteria,
            name="rap",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        response = self.get_genres()
        genre_json_list = response.json()[RESPONSE_KEYS.RESULTS]
        assert len(genre_json_list) == 2
