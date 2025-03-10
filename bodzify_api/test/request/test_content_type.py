import json


from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_double_encoded_json_then_error(self):
        data = json.dumps({"file": "https://example.com/file.mp3"})
        response = self.api_client.post(
            path=f'/api/{settings.APP_VERSION}/genres/', data=data, content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['details']['code'] == 'parse_error'

    def test_missing_content_type_then_error(self):
        response = self.api_client.post(
            path=f'/api/{settings.APP_VERSION}/genres/', data={}, format='', content_type='')

        assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        assert response.json()['details']['code'] == 'unsupported_media_type'
