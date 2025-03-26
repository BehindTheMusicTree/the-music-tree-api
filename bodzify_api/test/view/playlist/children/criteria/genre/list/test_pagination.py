
from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.view.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_page_provided_then_used(self):
        rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Rockabilly", parent=rock)
        self.model_fixture_factory.create_genre(name="Koko", parent=rock)
        genre_playlist_count = 4  # 3 genres + 1 genreless playlist

        print("\n--- Debug Info for test_page_provided_then_used ---")
        print(f"Expected genre_playlist_count: {genre_playlist_count}")

        # Get without page param for comparison
        no_page_response = self._list_genre_playlists()
        no_page_data = no_page_response.json()
        print(f"Without page param - results count: {len(no_page_data['results'])}")
        print(f"Without page param - results: {[r.get('name', 'genreless') for r in no_page_data['results']]}")

        # Test with page param
        response = self._list_genre_playlists(page=1)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        actual_results_count = len(response_data["results"])
        print(f"With page=1 - results count: {actual_results_count}")
        print(f"With page=1 - results: {[r.get('name', 'genreless') for r in response_data['results']]}")
        print(f"All response data: {response_data}")
        print("--- End Debug Info ---")

        assert actual_results_count == genre_playlist_count
        assert response_data["page"] == 1
        assert response_data["pageSize"] == settings.PAGINATION_PAGE_SIZE_DEFAULT
        assert response_data["totalPages"] == 1
        assert response_data["overallTotal"] == genre_playlist_count
