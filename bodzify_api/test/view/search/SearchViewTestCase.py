#!/usr/bin/env python

from django.urls import reverse

from rest_framework import status

from bodzify_api.test.view.ViewTestCase import ViewTestCase


class SearchViewTestCase(ViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewSearchData']

    def search(self, query):
        return self.apiClient.get(
            path=reverse('search', kwargs={'query':query}))

    def test_search(self):
        self.login(self.testUser)
        
        response = self.search()
        assert response.status_code == status.HTTP_200_OK
        
        response = self.search("All")
        assert response.content.overall_total == 1

        # Test non case-sensitiveness
        response = self.search("Rap")
        assert response.content.overall_total == 2

        # Test query in artist, album or title
        response = self.search("Sum")
        assert response.content.overall_total == 3

        # Test query returning playlist and track
        response = self.search("metal")
        assert response.content.overall_total == 2
