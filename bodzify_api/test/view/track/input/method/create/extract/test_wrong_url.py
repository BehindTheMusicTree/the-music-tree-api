#!/usr/bin/env python
from rest_framework import status

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class WringUrlTestCase(ApiViewTestCase):

    def test(self):
        track_url = ("https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3")
        data = {
            "url": track_url
        }
        response = self.extract(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
