#!/usr/bin/env python
from bodzify_api.test.view.modelless.SearchViewTestCase import SearchViewTestCase

class SearchViewTestCase3(SearchViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewSearchData3']

    """
    Test non case-sensitiveness. Thus the search "Rap" must return 2 entries (in this order 
    because of the name):
        - the "Rap" playlist;
        - the "US rap" playlist.
    """
    def test_search3(self):
        self.login(self.testUser)

        responseJson = self.search("Rap").json()
        results = responseJson['results']
        assert responseJson['overall_total'] == 2
        assert results['Playlist'][0]['name'] == "Rap"
        assert results['Playlist'][1]['name'] == "US rap"
