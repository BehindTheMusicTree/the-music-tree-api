
from rest_framework import status

from bodzify_api.model.criteria.Criteria import Fields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_root(self):
        genre = self.model_fixture_factory.create_genre(name="Rock")
        response = self._get_genres()
        assert response.status_code == status.HTTP_200_OK
        genre_json = self.results[0]
        assert genre_json[Fields.ROOT][Fields.UUID] == genre.uuid

    def test_root_of_first_descandant(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        response = self._get_genres()
        assert response.status_code == status.HTTP_200_OK
        for json_element in self.results:
            if json_element[Fields.UUID] == punk_genre.uuid:
                assert json_element[Fields.ROOT][Fields.UUID] == rock_genre.uuid

    def test_root_of_second_descandant(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk Hardcore", parent=punk_genre)
        response = self._get_genres()
        assert response.status_code == status.HTTP_200_OK
        for json_element in self.results:
            if json_element[Fields.UUID] == punkhardcore_genre.uuid:
                assert json_element[Fields.ROOT][Fields.UUID] == rock_genre.uuid
