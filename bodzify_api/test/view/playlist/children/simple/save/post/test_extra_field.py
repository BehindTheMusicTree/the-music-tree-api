#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.test.ApiTestCase import ApiTestCase
from django.urls import get_resolver


class TestCase(ApiTestCase):

    def test_error(self):
        print(get_resolver(None).reverse_dict.keys())
        data = {
            'nonExistingField': 'oifjqoif'
        }
        response = self.post_simple_playlist(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
