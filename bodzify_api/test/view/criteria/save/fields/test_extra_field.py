#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_error(self):
        data_dict = {
            "notExistingField": "Koko"
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
