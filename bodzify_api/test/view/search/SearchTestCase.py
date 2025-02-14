from django.urls import reverse

from bodzify_api.test.ApiTestCase import ApiTestCase


class SearchTestCase(ApiTestCase):
    def _search(self, **kwargs):
        return self.api_client.get(
            path=reverse('search-list'),
            data=kwargs,
            handle_response=self._set_results
        )

    def _post_search(self, **kwargs):
        return self.api_client.post(
            path=reverse('search-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _put_search(self, **kwargs):
        return self.api_client.put(
            path=reverse('search-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )
