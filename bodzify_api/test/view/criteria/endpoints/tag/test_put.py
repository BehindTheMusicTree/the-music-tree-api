from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_ok(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        genre_new_name = "Punk"
        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.NAME_PUBLIC: genre_new_name})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.name == genre_new_name
