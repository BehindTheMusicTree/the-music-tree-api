#!/usr/bin/env python
from bodzify_api.test.view.search.SearchViewTestCase import SearchViewTestCase

class SearchViewTestCase1(SearchViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewSearchData1']

    def test_search1(self):
        self.login(self.testUser)

        """
        - Test query returning playlist and track
        """
        response = self.search("metal")
        assert response.json()["overall_total"] == 2
