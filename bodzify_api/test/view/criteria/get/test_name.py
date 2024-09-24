#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.criteria.Criteria import AttributesLabel, Criteria
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)
        response = self.get_genres()
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        rock_genre_json = self.results[0]
        assert rock_genre_json[AttributesLabel.NAME] == genre_name
