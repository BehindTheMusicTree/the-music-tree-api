from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.Fields import Fields as Fields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase
from bodzify_api.test.view.track.input.method.put.fields.NotNullableFieldTestCase import NotNullableFieldTestCase


class TestCase(GenreTestCase, NotNullableFieldTestCase):

    def test_parent_none_then_root_itself(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)

        response = self._put_genre(uuid=punk_genre.uuid, **{Fields.PARENT: None})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.root == self.saved_genre

    def test_one_acendant_then_root_is_parent(self):
        rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._post_genre(**{Fields.NAME: "Punk", Fields.PARENT: rock.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == rock

    def test_two_acendant_then_root_is_parent_of_parent(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)

        response = self._post_genre(**{Fields.NAME: "Punk hardcore", Fields.PARENT: punk_genre.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == rock_genre

    def test_three_acendants_then_root_is_parent_of_parent_of_parent(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        hardcorepunk_genre = self.model_fixture_factory.create_genre(name="Hardcore Punk", parent=punk_genre)

        response = self._post_genre(**{Fields.NAME: "Punk hardcore japonais", Fields.PARENT: hardcorepunk_genre.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == rock_genre
