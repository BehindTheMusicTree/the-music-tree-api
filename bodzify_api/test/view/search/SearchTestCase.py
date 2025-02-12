
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class SearchTestCase(ApiTestCase):

    def _search(self, **kwargs):
        response = self.api_client.get(path=reverse('search-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _post_search(self, **kwargs):
        response = self.api_client.post(path=reverse('search-list'),
                                        data=kwargs,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_result(response)
        return response

    def _put_search(self, **kwargs):
        response = self.api_client.put(path=reverse('search-list'),
                                       data=kwargs,
                                       content_type='application/x-www-form-urlencoded')
        return response
