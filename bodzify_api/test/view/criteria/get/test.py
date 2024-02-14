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
        genresJsonList = response.json()[RESPONSE_KEYS.RESULTS]
        assert len(genresJsonList) == 1
        rock_genreJson = genresJsonList[0]
        assert rock_genreJson[Criteria.NAME] == genre_name
        assert rock_genreJson[Criteria.TYPE] == CriteriaTypesId.GENRE

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
        genresJsonList = response.json()[RESPONSE_KEYS.RESULTS]
        assert len(genresJsonList) == 2
