from uuid import UUID
from rest_framework import status

from bodzify_api.model.criteria.Criteria import Fields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_root(self):
        genre = self.model_fixture_factory.create_genre(name="Rock")
        response = self._retrieve_genre(uuid=genre.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert UUID(self.result[Fields.ROOT][Fields.UUID]) == genre.uuid

    def test_root_of_first_descendant(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        response = self._retrieve_genre(uuid=punk_genre.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert UUID(self.result[Fields.ROOT][Fields.UUID]) == rock_genre.uuid

    def test_root_of_second_descendant(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        ska_genre = self.model_fixture_factory.create_genre(name="Ska", parent=punk_genre)
        response = self._retrieve_genre(uuid=ska_genre.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert UUID(self.result[Fields.ROOT][Fields.UUID]) == rock_genre.uuid
