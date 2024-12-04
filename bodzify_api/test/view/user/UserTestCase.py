from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class UserTestCase(ApiTestCase):

    def _post_user(self, **kwargs):
        response = self.api_client.post(path=reverse('user-list'),
                                        data=kwargs,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_result(response)
        return response

    def _get_users(self):
        response = self.api_client.get(path=reverse('user-list'))
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _retrieve_user(self, pk: int):
        response = self.api_client.get(path=reverse('user-detail', kwargs={'pk': pk}))
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response

    def _put_user(self, pk: int, **kwargs):
        response = self.api_client.put(path=reverse('user-detail', kwargs={'pk': pk}),
                                       data=kwargs,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response

    def _delete_user(self, pk: int):
        return self.api_client.delete(path=reverse('user-detail', kwargs={'pk': pk}))
