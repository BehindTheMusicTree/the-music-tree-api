#!/usr/bin/env python

from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.view.ApiViewTestCase import RESPONSE_KEYS, ApiViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL

class TestCase(ApiViewTestCase):

    def test_root(self):
        genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CRITERIA_TYPES_ID.GENRE)
        response = self.get_genres()
        genre_json_list = response.json()[RESPONSE_KEYS.RESULTS]
        genre_json = genre_json_list[0]
        assert genre_json[ATTRIBUTES_LABEL.ROOT][ATTRIBUTES_LABEL.UUID] == genre.uuid

    def test_root_of_first_descandant(self):
        rock_genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria,
            name="Punk",
            user=self.test_user,
            type=CRITERIA_TYPES_ID.GENRE,
            parent=rock_genre)
        response = self.get_genres()
        genre_json_list = response.json()[RESPONSE_KEYS.RESULTS]
        for json_element in genre_json_list:
            if json_element[ATTRIBUTES_LABEL.UUID] == punk_genre.uuid:
                assert json_element[ATTRIBUTES_LABEL.ROOT][ATTRIBUTES_LABEL.UUID] == rock_genre.uuid

    def test_root_of_second_descandant(self):
        rock_genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria,
            name="Punk",
            user=self.test_user,
            type=CRITERIA_TYPES_ID.GENRE,
            parent=rock_genre)
        punk_hardcore_genre = G(Criteria,
            name="Punk Hardcore",
            user=self.test_user,
            type=CRITERIA_TYPES_ID.GENRE,
            parent=punk_genre)
        response = self.get_genres()
        genre_json_list = response.json()[RESPONSE_KEYS.RESULTS]
        for json_element in genre_json_list:
            if json_element[ATTRIBUTES_LABEL.UUID] == punk_hardcore_genre.uuid:
                assert json_element[ATTRIBUTES_LABEL.ROOT][ATTRIBUTES_LABEL.UUID] == rock_genre.uuid