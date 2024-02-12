#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api import settings


class TestCase(ApiViewTestCase):

    def test_errorWhenExtraField(self):
        data = {
            "notExistingField": "Koko"
        }
        response = self.post_genre(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST