import json
from django.urls import reverse
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
        path = reverse('genre-list')

        # Use the special test header to force the middleware to treat this as having no Content-Type
        response = self.api_client.post(
            path=path,
            data={},
            HTTP_X_TEST_FORCE_EMPTY_CONTENT_TYPE='true'
        )

        assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        assert response.json()['details']['code'] == 'unsupported_media_type'
