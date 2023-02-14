#!/usr/bin/env python
from bodzify_api.test.view.search.SearchViewTestCase import SearchViewTestCase

class SearchViewTestCase4(SearchViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewSearchData4']

    def test_search4(self):
        self.login(self.testUser)

        """
         - Test query in artist, album or title
        """
        response = self.search("Sum")
        assert response.content.overall_total == 3
