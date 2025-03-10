from rest_framework import status

from bodzify_api.test.view.search.SearchTestCase import SearchTestCase


class TestCase(SearchTestCase):

    def test_post_then_not_allowed(self):
        response = self._post_search()
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
