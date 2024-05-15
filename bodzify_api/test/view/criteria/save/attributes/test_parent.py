#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.CriteriaSchemaSerializer import FIELDS as INPUT_FIELDS
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_multiple_values_then_error(self):
        data = {
            INPUT_FIELDS.NAME: "Punk",
            INPUT_FIELDS.PARENT: ["value", "value2"]
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_then_none(self):
        data = {
            INPUT_FIELDS.NAME: "Punk",
            INPUT_FIELDS.PARENT: ""
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == None

    def test_existing(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        data = {
            INPUT_FIELDS.NAME: "Punk",
            INPUT_FIELDS.PARENT: rock_genre.uuid
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == rock_genre

    def test_error_when_not_existing(self):
        self.model_fixture_factory.create_genre(name="Rock")
        data = {
            INPUT_FIELDS.NAME: "Punk",
            INPUT_FIELDS.PARENT: "not existing"
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
