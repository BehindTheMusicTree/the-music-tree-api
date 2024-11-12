from rest_framework import status

from bodzify_api.serializer.schema.lib_track.input.endpoint.extract import Fields as ExtractFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test(self):
        data = {ExtractFields.URL: "https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3"}
        response = self._extract(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
