from uuid import UUID
from rest_framework import status

from bodzify_api.test.view.search.SearchTestCase import SearchTestCase


class TestCase(SearchTestCase):

    def test_retrieve_then_ok(self):
        response = self._retrieve_search(uuid=UUID('00000000-0000-0000-0000-000000000000'))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
