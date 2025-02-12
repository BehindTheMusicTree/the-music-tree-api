from rest_framework import status

from bodzify_api.serializer.schema.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from bodzify_api.test.view.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_combined_then_ok(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_punky = self.model_fixture_factory.create_genre(name="Punky", parent=genre_rock)

        response = self._get_genre_playlists(name='PU', parent=genre_rock.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert genre_punk.name in result_names
        assert genre_punky.name in result_names
