#!/usr/bin/env python
from bodzify_api.test.view.modelless.SearchViewTestCase import SearchViewTestCase

class SearchViewTestCase2(SearchViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewSearchData2']

    """
    The search "All" must return 2 results:
     - the "All" playlist;
     - the "We're All To Blame" track.
    """
    def test_search2(self):
        self.login(self.testUser)

        responseJson = self.search("All").json()
        results = responseJson['results']
        assert responseJson["overall_total"] == 2
        assert results["LibraryTrack"][0]['title'] == "We're All To Blame"
        assert results["Playlist"][0]['name'] == "All"
