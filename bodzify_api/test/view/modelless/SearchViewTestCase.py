#!/usr/bin/env python
from django.urls import reverse
from bodzify_api.test.view.ViewTestCase import ViewTestCase


class SearchViewTestCase(ViewTestCase):

    def search(self, query):
        return self.apiClient.get(path=reverse('search-list'), data={'query':query})
