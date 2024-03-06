#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_error(self):
        data = {
            "field_not_handled": "pofkefposkfwp"
        }
        response = self.extract_default_mine_track(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
