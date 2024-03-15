#!/usr/bin/env python

from ddf import G
from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL


class TestCase(ApiTestCase):

    def test_root(self):
        genre = G(Criteria,
                  name="Rock",
                  user=self.test_user,
                  type=CRITERIA_TYPES_ID.GENRE)
        response = self.get_genres()
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        genre_json = self.results[0]
        assert genre_json[ATTRIBUTES_LABEL.ROOT][ATTRIBUTES_LABEL.UUID] == genre.uuid  # type: ignore

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
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        for json_element in self.results:
            if json_element[ATTRIBUTES_LABEL.UUID] == punk_genre.uuid:  # type: ignore
                assert json_element[ATTRIBUTES_LABEL.ROOT][ATTRIBUTES_LABEL.UUID] == rock_genre.uuid  # type: ignore

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
        asseert = response.status_code == status.HTTP_200_OK  # type: ignore
        for json_element in self.results:
            if json_element[ATTRIBUTES_LABEL.UUID] == punk_hardcore_genre.uuid:  # type: ignore
                assert json_element[ATTRIBUTES_LABEL.ROOT][ATTRIBUTES_LABEL.UUID] == rock_genre.uuid  # type: ignore
