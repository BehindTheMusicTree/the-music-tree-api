#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.serializer.track.input.schema.LibTrackExtractSchemaSerializer import FIELDS as EXTRACT_FIELDS


class TestCase(ApiViewTestCase):

    def test(self):
        data = {
            EXTRACT_FIELDS.URL: "https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3"
        }
        response = self.extract(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
