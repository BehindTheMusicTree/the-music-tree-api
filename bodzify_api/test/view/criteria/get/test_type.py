#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.criteria.CriteriaType import CriteriaTypesLabel
from bodzify_api.serializer.criteria.output.detailed import Fields as GetFields
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)
        response = self.get_genres()
        assert response.status_code == status.HTTP_200_OK
        criteria_type_label = self.results[0][GetFields.TYPE][GetFields.TYPE_LABEL]
        assert criteria_type_label == CriteriaTypesLabel.GENRE
