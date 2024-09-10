#!/usr/bin/env python

import logging
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.AppTestCase import AppTestCase


class MineTestCase(AppTestCase):

    def search_mine(self, source, query):
        data_dict = {
            'source': source,
            'query': query
        }
        response = self.api_client.get(path=reverse('mine-track-list'),
                                       data=self._replace_none_values_by_empty_string(data_dict))
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response
