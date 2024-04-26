#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.CriteriaSchemaSerializer import FIELDS as POST_FIELDS
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_multiple_values_then_error(self):
        data = {
            POST_FIELDS.NAME: "Punk",
            POST_FIELDS.PARENT: ["value", "value2"]
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_empty_then_none(self):
        data = {
            POST_FIELDS.NAME: "Punk",
            POST_FIELDS.PARENT: ""
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_genre.parent == None

    def test_existing(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        data = {
            POST_FIELDS.NAME: "Punk",
            POST_FIELDS.PARENT: rock_genre.uuid  # type: ignore
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_genre.parent == rock_genre

    def test_error_when_not_existing(self):
        G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        data = {
            POST_FIELDS.NAME: "Punk",
            POST_FIELDS.PARENT: "not existing"
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
