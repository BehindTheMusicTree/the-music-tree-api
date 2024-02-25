#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_error(self):
        data = {
            "fieldNotHandled": "pofkefposkfwp"
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
