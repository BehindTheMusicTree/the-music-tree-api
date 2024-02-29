#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_errorWhenExtraField(self):
        data = {
            "notExistingField": "Koko"
        }
        response = self.post_genre(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST