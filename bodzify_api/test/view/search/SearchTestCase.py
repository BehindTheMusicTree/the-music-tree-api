from urllib.parse import urlencode
from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class SearchTestCase(ApiTestCase):

    def _post_search(self, **kwargs):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(kwargs), doseq=True)
        response = self.api_client.post(path=reverse('search-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_result(response)
        return response

    def _search(self, query):
        response = self.api_client.get(path=reverse('search-list'), data={'query': query})
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _retrieve_search(self, uuid: UUID):
        return self.api_client.delete(path=reverse('search-detail', kwargs={'pk': uuid}))

    def _put_search(self, uuid: UUID, **kwargs):
        data_url_encoded = urlencode(query=self._replace_none_values_by_empty_string(kwargs), doseq=True)
        response = self.api_client.put(path=reverse('search-detail', kwargs={'pk': uuid}),
                                       data=data_url_encoded,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response
