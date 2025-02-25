from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import \
    CriteriaPlaylist
from bodzify_api.serializer.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_new_root_then_update_root_of_descendants(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=genre_punk)
        frenchhardcore_genre = self.model_fixture_factory.create_genre(name="French hardcore",
                                                                       parent=punkhardcore_genre)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})
        assert response.status_code == status.HTTP_200_OK

        root_playlist = genre_rock.criteria_playlist

        updated_genre_punk_playlist: CriteriaPlaylist = \
            CriteriaPlaylist.objects.get(user=self.test_user1, criteria=genre_punk)
        assert updated_genre_punk_playlist.root == root_playlist

        updated_punkhardcore_genre_playlist: CriteriaPlaylist =\
            CriteriaPlaylist.objects.get(user=self.test_user1, criteria=punkhardcore_genre)
        assert updated_punkhardcore_genre_playlist.root == root_playlist

        updated_frenchhardcore_genre_playlist: CriteriaPlaylist = \
            CriteriaPlaylist.objects.get(user=self.test_user1, criteria=frenchhardcore_genre)
        assert updated_frenchhardcore_genre_playlist.root == root_playlist
