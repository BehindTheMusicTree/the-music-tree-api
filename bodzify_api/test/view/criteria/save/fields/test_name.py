#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api import settings


class TestCase(ApiViewTestCase):

    def test_longest(self):
        genre_name = "a" * settings.CRITERIA_NAME_LENGTH_MAX
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: genre_name
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.name == genre_name

    def test_error_too_long(self):
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "a" * (settings.CRITERIA_NAME_LENGTH_MAX + 1)
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
