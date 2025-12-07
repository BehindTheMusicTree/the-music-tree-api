
from rest_framework import status

from api import settings
from api.test.integration.view.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_page_provided_then_used(self):
        rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Rockabilly", parent=rock)
        self.model_fixture_factory.create_genre(name="Koko", parent=rock)

        total_genre_playlist_count = 4  # 3 genres + 1 genreless playlist

        response = self._list_genre_playlists(page=1)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        actual_results_count = len(response_data["results"])

        assert actual_results_count == total_genre_playlist_count
        assert response_data["page"] == 1
        assert response_data["pageSize"] == settings.PAGINATION_PAGE_SIZE_DEFAULT
        assert response_data["totalPages"] == 1
        assert response_data["overallTotal"] == total_genre_playlist_count
