from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.endpoint.extract import Fields as ExtractFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test(self):
        data = {ExtractFields.URL: "https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3"}
        response = self._extract(**data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
