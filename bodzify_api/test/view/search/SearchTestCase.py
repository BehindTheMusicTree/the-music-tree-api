#!/usr/bin/env python


from django.urls import reverse
from rest_framework import status

from bodzify_api.test.AppTestCase import AppTestCase


class SearchTestCase(AppTestCase):

    def _search(self, query):
        response = self.api_client.get(path=reverse('search-list'), data={'query': query})
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response
