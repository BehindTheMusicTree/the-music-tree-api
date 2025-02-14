from rest_framework import status

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_from_being_root_to_first_descendant(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.root == genre_rock

    def test_from_being_first_descendant_to_root(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: ""})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.root == genre_punk

    def test_new_root_then_update_root_of_descendants(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=genre_punk)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.root == genre_rock
        updated_punkhardcore_genre = Criteria.objects.get(user=self.test_user1, uuid=punkhardcore_genre.uuid)
        assert updated_punkhardcore_genre.root == genre_rock

    def test_new_ascendant_then_update_root_of_self_and_descendants(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=genre_punk)
        frenchpunkhardcore_genre = self.model_fixture_factory.create_genre(name="French punk hardcore",
                                                                           parent=punkhardcore_genre)
        bretonpunkhardcore_genre = self.model_fixture_factory.create_genre(name="Breton punk hardcore",
                                                                           parent=frenchpunkhardcore_genre)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.root == genre_rock
        updated_punkhardcore_genre: Criteria = Criteria.objects.get(user=self.test_user1, uuid=punkhardcore_genre.uuid)
        assert updated_punkhardcore_genre.root == genre_rock
        updated_frenchpunkhardcore_genre: Criteria = \
            Criteria.objects.get(user=self.test_user1, uuid=frenchpunkhardcore_genre.uuid)
        assert updated_frenchpunkhardcore_genre.root == genre_rock
        updated_bretonpunkhardcore_genre: Criteria = \
            Criteria.objects.get(user=self.test_user1, uuid=bretonpunkhardcore_genre.uuid)
        assert updated_bretonpunkhardcore_genre.root == genre_rock

    def test_newly_root_then_update_root_of_descendants(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=genre_punk)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: ""})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.root == genre_punk
        updated_punkhardcore_genre: Criteria = Criteria.objects.get(user=self.test_user1, uuid=punkhardcore_genre.uuid)
        assert updated_punkhardcore_genre.root == genre_punk
