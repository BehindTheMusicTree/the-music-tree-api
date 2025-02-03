from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.post import Fields as PostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_extra_field_then_error(self):
        genre = self.model_fixture_factory.create_genre(name="Rock")
        response = self._put_genre(uuid=genre.uuid, **{PostFields.NAME_PUBLIC: "Rock", "extra_field": "extra_value"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
