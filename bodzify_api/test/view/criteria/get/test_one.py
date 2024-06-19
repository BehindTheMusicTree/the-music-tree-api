#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_two(self):
        self.model_fixture_factory.create_genre(name="rock")
        response = self.get_genres()
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
