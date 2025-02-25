from uuid import UUID

import pytest
from django.urls import NoReverseMatch, reverse

from bodzify_api.test.view.search.SearchTestCase import SearchTestCase


class TestCase(SearchTestCase):

    def test_retrieve_then_url_not_found(self):
        with pytest.raises(NoReverseMatch):
            reverse('search-detail', kwargs={'pk': UUID('00000000-0000-0000-0000-000000000000')})