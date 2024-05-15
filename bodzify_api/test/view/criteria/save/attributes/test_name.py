#!/usr/bin/env python

from rest_framework import status
from bodzify_api.serializer.criteria.input.schema.CriteriaSchemaSerializer import FIELDS as INPUT_FIELDS
from bodzify_api import settings
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_longest(self):
        genre_name = "a" * settings.CRITERIA_NAME_LEN_MAX
        data = {INPUT_FIELDS.NAME: genre_name}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.name == genre_name

    def test_error_too_long(self):
        data = {INPUT_FIELDS.NAME: "a" * (settings.CRITERIA_NAME_LEN_MAX + 1)}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_multiple_values_then_error(self):
        data = {INPUT_FIELDS.NAME: ["value", "value2"]}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
