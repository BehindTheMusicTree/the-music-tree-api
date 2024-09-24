#!/usr/bin/env python

from rest_framework import status

from bodzify_api.serializer.track.input.endpoint.extract import Fields as EXTRACT_FIELDS
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test(self):
        data = {EXTRACT_FIELDS.URL: "https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3"}
        response = self.extract(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
