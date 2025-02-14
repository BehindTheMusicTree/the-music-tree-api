
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class SearchTestCase(ApiTestCase):

    def _search(self, **kwargs):
        return self.api_client.get(
            path=reverse('search-list'),
            data=kwargs,
            on_success=self._set_results_attributes,
            on_bad_request=self._set_bad_request_result
        )

    def _post_search(self, **kwargs):
        return self.api_client.post(
            path=reverse('search-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _put_search(self, **kwargs):
        return self.api_client.put(
            path=reverse('search-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )
