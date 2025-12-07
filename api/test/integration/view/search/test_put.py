
from rest_framework import status

from api.test.integration.view.search.SearchTestCase import SearchTestCase


class TestCase(SearchTestCase):

    def test_put_then_405(self):
        response = self._put_search(query='test')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
