#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_not_provided_then_none(self):
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Rock"
        }
        response = self.post_genre(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == None

    def test_empty_then_none(self):
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Rock",
            CRITERIA_ATTRIBUTES_LABEL.PARENT: ""
        }
        response = self.post_genre(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == None
