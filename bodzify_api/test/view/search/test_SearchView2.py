#!/usr/bin/env python
from bodzify_api.test.view.search.SearchViewTestCase import SearchViewTestCase

class SearchViewTestCase2(SearchViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewSearchData2']

    def test_search2(self):
        self.login(self.testUser)

        response = self.search("All")
        assert response.content.overall_total == 1
