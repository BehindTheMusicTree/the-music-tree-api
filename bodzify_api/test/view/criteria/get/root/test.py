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
        genresJsonList = response.json()[RESPONSE_KEYS.RESULTS]
        genreJson = genresJsonList[0]
        assert genreJson[Criteria.ROOT] == genre.uuid

    def test_not_root(self):
        rock_genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        punkGenre = G(Criteria,
            name="Punk",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        response = self.get_genres()
        genresJsonList = response.json()[RESPONSE_KEYS.RESULTS]
        for jsonElement in genresJsonList:
            if jsonElement[Criteria.UUID] == punkGenre.uuid:
                assert jsonElement[Criteria.ROOT] == rock_genre.uuid