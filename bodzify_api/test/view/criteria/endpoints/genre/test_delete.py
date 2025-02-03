from rest_framework import status

from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_delete_then_error(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        response = self._delete_genre(uuid=genre.uuid)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
