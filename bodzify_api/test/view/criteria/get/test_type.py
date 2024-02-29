#!/usr/bin/env python

from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID, \
    ATTRIBUTES_LABEL as CRITERIA_TYPE_ATTRIBUTES_LABEL, \
    CRITERIA_TYPES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL, Criteria


class TestCase(ApiViewTestCase):

    def test(self):
        genre_name = "Rock"
        genre = G(Criteria,
                  name=genre_name,
                  user=self.test_user,
                  type=CRITERIA_TYPES_ID.GENRE)
        response = self.get_genres()
        genre_json_list = response.json()[ApiViewTestCase.RESPONSE_FIELDS.RESULTS]
        rock_genre_json = genre_json_list[0]
        criteria_type_label = rock_genre_json[ATTRIBUTES_LABEL.TYPE][CRITERIA_TYPE_ATTRIBUTES_LABEL.LABEL]
        assert criteria_type_label == CRITERIA_TYPES_LABEL.GENRE
