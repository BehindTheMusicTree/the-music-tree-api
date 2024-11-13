from urllib.parse import urlencode
from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class AllLibTracksMixinTestCase(ApiTestCase):

    def _post_all_lib_tracks_mixin(self, **kwargs):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(**kwargs), doseq=True)
        response = self.api_client.post(path=reverse('all-library-tracks-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_result(response)
        return response

    def _get_all_lib_tracks_mixin(self, **kwargs):
        response = self.api_client.get(path=reverse('all-library-tracks-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response

    def _retrieve_all_lib_tracks_mixin(self, uuid: UUID):
        return self.api_client.delete(path=reverse('all-library-tracks-detail', kwargs={'pk': uuid}))

    def _put_all_lib_tracks_mixin(self, uuid: UUID):
        return self.api_client.get(path=reverse('all-library-tracks-detail', kwargs={'pk': uuid}))

    def _delete_all_lib_tracks_mixin(self, uuid: UUID):
        return self.api_client.delete(path=reverse('all-library-tracks-detail', kwargs={'pk': uuid}))
