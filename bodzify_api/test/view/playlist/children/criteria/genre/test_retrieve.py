from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from bodzify_api.test.view.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_retrieve_then_ok(self):
        rock_criteria_name = "Rock"
        genre_rock = self.model_fixture_factory.create_genre(name=rock_criteria_name)
        rock_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=genre_rock)

        response = self._retrieve_genre_playlist(uuid=rock_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[RietrieveFields.NAME] == rock_criteria_name
