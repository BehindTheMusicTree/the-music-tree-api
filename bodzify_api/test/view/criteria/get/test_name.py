#!/usr/bin/env python

from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.view.ApiViewTestCase import RESPONSE_KEYS, ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL, Criteria

class TestCase(ApiViewTestCase):

    def test(self):
        genre_name = "Rock"
        G(Criteria,
            name=genre_name,
            user=self.test_user,
            type=CRITERIA_TYPES_ID.GENRE)
        response = self.get_genres()
        genre_json_list = response.json()[RESPONSE_KEYS.RESULTS]
        assert len(genre_json_list) == 1
        rock_genre_json = genre_json_list[0]
        assert rock_genre_json[ATTRIBUTES_LABEL.NAME] == genre_name
