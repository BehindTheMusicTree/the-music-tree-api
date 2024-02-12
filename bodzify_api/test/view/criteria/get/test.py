#!/usr/bin/env python

from ddf import G
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.test.view.ApiViewTestCase import RESPONSE_KEYS, ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as Criteria

class TestCase(ApiViewTestCase):

    def test(self):
        genreName = "Rock"
        genre = G(Criteria,
                      name=genreName,
                      user=self.test_user,
                      type=CriteriaTypesId.GENRE)
        response = self.get_genres()
        genresJsonList = response.json()[RESPONSE_KEYS.RESULTS]
        assert len(genresJsonList) == 1
        rockGenreJson = genresJsonList[0]
        assert rockGenreJson[Criteria.NAME] == genreName
        assert rockGenreJson[Criteria.TYPE] == CriteriaTypesId.GENRE

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
