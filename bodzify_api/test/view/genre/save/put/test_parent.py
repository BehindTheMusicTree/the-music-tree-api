from rest_framework import status

from bodzify_api.serializer.schema.criteria.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_not_provided_then_unchanged(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        response = self._put_genre(uuid=punk_genre.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.parent == rock_genre

    def test_error_when_parent_is_one_of_descendants(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=punk_genre)

        data = {PutFields.PARENT: punkhardcore_genre.uuid}
        response = self._put_genre(uuid=rock_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_error_when_parent_is_itself(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        data = {PutFields.PARENT: rock_genre.uuid}
        response = self._put_genre(uuid=rock_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
