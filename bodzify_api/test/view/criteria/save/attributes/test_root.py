from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.Fields import Fields as Fields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.test.view.track.input.method.put.fields.NotNullableFieldTestCase import NotNullableFieldTestCase


class TestCase(GenreTestCase, NotNullableFieldTestCase):

    def test_parent_none_then_root_itself(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._put_genre(uuid=genre_punk.uuid, **{Fields.PARENT: None})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.root == self.saved_genre

    def test_one_acendant_then_root_is_parent(self):
        rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk", Fields.PARENT: rock.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.root == rock

    def test_two_acendant_then_root_is_parent_of_parent(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk hardcore", Fields.PARENT: genre_punk.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.root == genre_rock

    def test_three_acendants_then_root_is_parent_of_parent_of_parent(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        hardcoregenre_punk = self.model_fixture_factory.create_genre(name="Hardcore Punk", parent=genre_punk)

        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk hardcore japonais",
                                    Fields.PARENT: hardcoregenre_punk.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.root == genre_rock
