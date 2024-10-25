#!/usr/bin/env python

from urllib.parse import urlencode
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class UserViewTestCase(ApiTestCase):

    def _login_as_test_admin_and_delete_user(self, user_pk: str):
        self._login_as_test_admin()
        response = self.api_client.delete(path=reverse('user-detail', kwargs={'pk': user_pk}))
        return response

    def _login_as_test_admin_and_get_user(self):
        response = self.api_client.get(path=reverse('user-list'))
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _login_as_test_admin_and_retrieve_user(self, user_pk: str):
        response = self.api_client.get(path=reverse('user-detail', kwargs={'pk': user_pk}))
        return response

    def _login_as_test_admin_and_post_user(self, data_dict):
        self._login_as_test_admin()
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.post(path=reverse('user-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        return response
