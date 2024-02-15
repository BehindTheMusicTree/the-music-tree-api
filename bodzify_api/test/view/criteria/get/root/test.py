#!/usr/bin/env python
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.test.view.ApiViewTestCase import RESPONSE_KEYS, ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as Criteria

class TestCase(ApiViewTestCase):

    def test_root(self):
        genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        response = self.get_genres()
        genre_json_list = response.json()[RESPONSE_KEYS.RESULTS]
        genre_json = genre_json_list[0]
        assert genre_json[Criteria.ROOT] == genre.uuid

    def test_not_root(self):
        rock_genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        punk_genre = G(Criteria,
            name="Punk",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        response = self.get_genres()
        genre_json_list = response.json()[RESPONSE_KEYS.RESULTS]
        for json_element in genre_json_list:
            if json_element[Criteria.UUID] == punk_genre.uuid:
                assert json_element[Criteria.ROOT] == rock_genre.uuid