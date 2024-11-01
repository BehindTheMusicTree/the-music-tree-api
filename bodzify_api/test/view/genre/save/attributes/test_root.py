
from rest_framework import status

from bodzify_api.serializer.schema.criteria.input.schema.schema import Fields as InputFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_parent_none_then_root_itself(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        data = {InputFields.PARENT: None}
        response = self._put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.root == self.saved_genre

    def test_one_acendant_then_root_is_parent(self):
        rock = self.model_fixture_factory.create_genre(name="Rock")
        data = {
            InputFields.NAME: "Punk",
            InputFields.PARENT: rock.uuid
        }
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == rock

    def test_two_acendant_then_root_is_parent_of_parent(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        data = {
            InputFields.NAME: "Punk hardcore",
            InputFields.PARENT: punk_genre.uuid
        }
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == rock_genre

    def test_three_acendants_then_root_is_parent_of_parent_of_parent(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        hardcorepunk_genre = self.model_fixture_factory.create_genre(name="Hardcore Punk", parent=punk_genre)
        data = {
            InputFields.NAME: "Punk hardcore japonais",
            InputFields.PARENT: hardcorepunk_genre.uuid
        }
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == rock_genre
