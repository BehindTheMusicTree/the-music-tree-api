from rest_framework import status

from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_no_field_specified_then_error(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._put_genre(uuid=genre_rock.uuid)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
