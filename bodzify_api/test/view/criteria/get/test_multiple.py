#!/usr/bin/env python

from ddf import G
from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.model.criteria.Criteria import Criteria


class TestCase(ApiTestCase):

    def test_two(self):
        G(Criteria,
            name="rock",
            user=self.test_user,
            type=CRITERIA_TYPES_ID.GENRE)
        G(Criteria,
            name="rap",
            user=self.test_user,
            type=CRITERIA_TYPES_ID.GENRE)
        response = self.get_genres()
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.overall_total == 2
