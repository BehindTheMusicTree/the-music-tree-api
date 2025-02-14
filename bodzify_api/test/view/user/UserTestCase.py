
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class UserTestCase(ApiTestCase):

    def _post_user(self, **kwargs):
        return self.api_client.post(
            path=reverse('user-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _get_users(self):
        return self.api_client.get(
            path=reverse('user-list'),
            on_success=self._set_results_attributes,
            on_bad_request=self._set_bad_request_result
        )

    def _retrieve_user(self, pk: int):
        return self.api_client.get(
            path=reverse('user-detail', kwargs={'pk': pk}),
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _put_user(self, pk: int, **kwargs):
        return self.api_client.put(
            path=reverse('user-detail', kwargs={'pk': pk}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _delete_user(self, pk: int):
        return self.api_client.delete(path=reverse('user-detail', kwargs={'pk': pk}))
