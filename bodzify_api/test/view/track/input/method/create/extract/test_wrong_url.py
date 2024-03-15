#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.serializer.track.input.schema.LibTrackExtractSchemaSerializer import FIELDS as EXTRACT_FIELDS


class TestCase(ApiTestCase):

    def test(self):
        data = {
            EXTRACT_FIELDS.URL: "https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3"
        }
        response = self.extract(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
