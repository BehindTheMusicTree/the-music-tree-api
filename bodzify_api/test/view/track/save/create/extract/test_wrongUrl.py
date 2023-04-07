#!/usr/bin/env python
from rest_framework import status

from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class WringUrlTestCase(TrackViewTestCase):

    def test(self):
        trackUrl = ("https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3")
        data = {
            "url": trackUrl
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
