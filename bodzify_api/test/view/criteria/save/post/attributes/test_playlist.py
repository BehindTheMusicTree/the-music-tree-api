from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import \
    CriteriaPlaylist
from bodzify_api.serializer.model.criteria.input.post import \
    Fields as PostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_playlist_creation(self):
        genre_name = "Rock"
        response = self._post_genre(**{PostFields.NAME_PUBLIC: genre_name})
        assert response.status_code == status.HTTP_201_CREATED
        assert CriteriaPlaylist.objects.filter(user=self.test_user1, criteria__name=genre_name).exists()

    def test_playlist_root(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        punkhardcore_genre_name = "Punk Hardcore"
        data = {PostFields.NAME_PUBLIC: punkhardcore_genre_name, PostFields.PARENT: genre_punk.uuid}
        response = self._post_genre(**data)
        assert response.status_code == status.HTTP_201_CREATED
        punkhardcore_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=punkhardcore_genre_name)
        assert punkhardcore_playlist.root == genre_rock.criteria_playlist
