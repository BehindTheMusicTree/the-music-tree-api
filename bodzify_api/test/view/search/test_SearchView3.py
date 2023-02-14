#!/usr/bin/env python
from bodzify_api.test.view.search.SearchViewTestCase import SearchViewTestCase

class SearchViewTestCase3(SearchViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewSearchData3']

    def test_search3(self):
        self.login(self.testUser)

        """
        - Test non case-sensitiveness
        """
        response = self.search("Rap")
        assert response.content.overall_total == 2
