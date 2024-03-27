#!/usr/bin/env python

from ddf import G
from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL, Criteria
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test(self):
        genre_name = "Rock"
        G(Criteria, name=genre_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        response = self.get_genres()
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.overall_total == 1
        rock_genre_json = self.results[0]
        assert rock_genre_json[ATTRIBUTES_LABEL.NAME] == genre_name
