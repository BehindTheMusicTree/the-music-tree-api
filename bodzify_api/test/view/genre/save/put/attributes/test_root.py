from rest_framework import status

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.model.criteria.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_from_being_root_to_first_descendant(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk")

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: rock_genre.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.root == rock_genre

    def test_from_being_first_descendant_to_root(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: ""})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.root == punk_genre

    def test_new_root_then_update_root_of_descendants(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=punk_genre)

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: rock_genre.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.root == rock_genre
        updated_punkhardcore_genre = Criteria.objects.get(user=self.test_user1, uuid=punkhardcore_genre.uuid)
        assert updated_punkhardcore_genre.root == rock_genre

    def test_new_ascendant_then_update_root_of_self_and_descendants(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=punk_genre)
        frenchpunkhardcore_genre = self.model_fixture_factory.create_genre(name="French punk hardcore",
                                                                           parent=punkhardcore_genre)
        bretonpunkhardcore_genre = self.model_fixture_factory.create_genre(name="Breton punk hardcore",
                                                                           parent=frenchpunkhardcore_genre)

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: rock_genre.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.root == rock_genre
        updated_punkhardcore_genre: Criteria = Criteria.objects.get(user=self.test_user1, uuid=punkhardcore_genre.uuid)
        assert updated_punkhardcore_genre.root == rock_genre
        updated_frenchpunkhardcore_genre: Criteria = \
            Criteria.objects.get(user=self.test_user1, uuid=frenchpunkhardcore_genre.uuid)
        assert updated_frenchpunkhardcore_genre.root == rock_genre
        updated_bretonpunkhardcore_genre: Criteria = \
            Criteria.objects.get(user=self.test_user1, uuid=bretonpunkhardcore_genre.uuid)
        assert updated_bretonpunkhardcore_genre.root == rock_genre

    def test_newly_root_then_update_root_of_descendants(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=punk_genre)

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: ""})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.root == punk_genre
        updated_punkhardcore_genre: Criteria = Criteria.objects.get(user=self.test_user1, uuid=punkhardcore_genre.uuid)
        assert updated_punkhardcore_genre.root == punk_genre
