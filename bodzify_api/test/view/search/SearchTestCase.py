from django.urls import reverse

from bodzify_api.test.utils.AppTestCase import AppTestCase


class SearchTestCase(AppTestCase):
    def _search(self, **kwargs):
        return self.api_client.get(path=reverse('search-list'), data=kwargs, handle_response=self._set_results)

    def _post_search(self, **kwargs):
        return self.api_client.post(path=reverse('search-list'),
                                    data=kwargs,
                                    content_type='application/json',
                                    handle_response=self._set_results)

    def _put_search(self, **kwargs):
        return self.api_client.put(path=reverse('search-list'),
                                   data=kwargs,
                                   content_type='application/json',
                                   handle_response=self._set_results)
