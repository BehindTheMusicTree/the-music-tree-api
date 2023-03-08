#!/usr/bin/env python
from bodzify_api.test.view.modelless.SearchViewTestCase import SearchViewTestCase

class SearchViewTestCase1(SearchViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewSearchData1']

    """
    The query "Sum" must return the following results:
     - the "Summer Love" track;
     - the "Sum 41" artist;
     - the "J'ai le Sum" album.
    """
    def test_search1(self):
        self._login(self.testUser)
        responseJson = self.search("Sum").json()
        assert responseJson['overall_total'] == 3
        results = responseJson['results']
        assert results['LibraryTrack'][0]['title'] == "Summer Love"
        assert results['Artist'][0]['name'] == "Sum 41"
        assert results['Album'][0]['name'] == "J'ai le Sum"
