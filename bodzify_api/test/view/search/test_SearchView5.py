#!/usr/bin/env python
from bodzify_api.test.view.search.SearchViewTestCase import SearchViewTestCase

class SearchViewTestCase5(SearchViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewSearchData5']

    def test_search5(self):
        self.login(self.testUser)
        
        """
        - Test query returning playlist and track
        """
        response = self.search("metal")
        assert response.content.overall_total == 2
