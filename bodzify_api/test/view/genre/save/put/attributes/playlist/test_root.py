from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.criteria.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_new_root_then_update_root_of_descendants(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=punk_genre)
        frenchhardcore_genre = self.model_fixture_factory.create_genre(name="French hardcore",
                                                                       parent=punkhardcore_genre)

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: rock_genre.uuid})
        assert response.status_code == status.HTTP_200_OK

        root_playlist = rock_genre.criteria_playlist

        updated_punk_genre_playlist: CriteriaPlaylist = \
            CriteriaPlaylist.objects.get(user=self.test_user1, criteria=punk_genre)
        assert updated_punk_genre_playlist.root == root_playlist

        updated_punkhardcore_genre_playlist: CriteriaPlaylist =\
            CriteriaPlaylist.objects.get(user=self.test_user1, criteria=punkhardcore_genre)
        assert updated_punkhardcore_genre_playlist.root == root_playlist

        updated_frenchhardcore_genre_playlist: CriteriaPlaylist = \
            CriteriaPlaylist.objects.get(user=self.test_user1, criteria=frenchhardcore_genre)
        assert updated_frenchhardcore_genre_playlist.root == root_playlist
