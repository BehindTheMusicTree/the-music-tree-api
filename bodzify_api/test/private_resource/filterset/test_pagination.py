
from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.integration.view.album.AlbumTestCase import AlbumTestCase


class TestCase(AlbumTestCase):

    def test_page_invalid_then_400_bad_request(self):
        response = self._list_albums(page=0)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert "Invalid page" in response_data["details"]["message"]

    def test_page_and_pagesize_not_provided_then_first_page_and_default_pagesize_are_used(self):
        for i in range(settings.PAGINATION_PAGE_SIZE_DEFAULT + 1):
            self.model_fixture_factory.create_album(name=f"Album {i}")

        response = self._list_albums()

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data["results"]) == settings.PAGINATION_PAGE_SIZE_DEFAULT
        assert response_data["page"] == 1
        assert response_data["pageSize"] == settings.PAGINATION_PAGE_SIZE_DEFAULT
        assert response_data["totalPages"] == 2
        assert response_data["overallTotal"] == settings.PAGINATION_PAGE_SIZE_DEFAULT + 1

    def test_page_and_pagesize_provided_then_page_and_pagesize_are_used_1(self):
        albums_count = 15
        for i in range(albums_count):
            self.model_fixture_factory.create_album(name=f"Album {i}")

        response = self._list_albums(page=2, pageSize=10)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data["results"]) == 5
        assert response_data["page"] == 2
        assert response_data["pageSize"] == 10
        assert response_data["totalPages"] == 2
        assert response_data["overallTotal"] == albums_count
