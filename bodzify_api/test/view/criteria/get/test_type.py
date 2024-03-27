#!/usr/bin/env python

from ddf import G
from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID, CRITERIA_TYPES_LABEL
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import FIELDS as GET_FIELDS
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test(self):
        genre_name = "Rock"
        G(Criteria, name=genre_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        response = self.get_genres()
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        criteria_type_label = self.results[0][GET_FIELDS.TYPE][GET_FIELDS.TYPE_LABEL]
        assert criteria_type_label == CRITERIA_TYPES_LABEL.GENRE
