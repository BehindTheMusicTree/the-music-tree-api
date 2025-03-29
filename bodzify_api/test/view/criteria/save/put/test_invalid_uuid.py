import uuid

from rest_framework import status

from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_malformed_uuid_then_400_bad_request(self):
        response = self._put_genre(uuid="invalid_uuid")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_nonexistent_uuid_then_404(self):
        response = self._put_genre(uuid=uuid.uuid4())

        assert response.status_code == status.HTTP_404_NOT_FOUND
