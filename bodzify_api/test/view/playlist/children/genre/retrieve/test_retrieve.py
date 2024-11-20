from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.playlist.children.criteria.output.detailed import Fields as GetResultFields
from bodzify_api.test.view.playlist.children.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_retrieve_then_ok(self):
        rock_criteria_name = "Rock"
        rock_genre = self.model_fixture_factory.create_genre(name=rock_criteria_name)
        rock_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=rock_genre)

        response = self._retrieve_genre_playlist(uuid=rock_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[GetResultFields.NAME] == rock_criteria_name
