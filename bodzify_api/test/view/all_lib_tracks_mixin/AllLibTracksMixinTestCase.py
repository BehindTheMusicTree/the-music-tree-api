from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class AllLibTracksMixinTestCase(ApiTestCase):

    def _post_all_lib_tracks_mixin(self, **kwargs):
        return self.api_client.post(
            path=reverse('all-library-tracks-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _get_all_lib_tracks_mixin(self, **kwargs):
        return self.api_client.get(
            path=reverse('all-library-tracks-list'),
            data=kwargs,
            on_success=self._set_results_attributes,
            on_bad_request=self._set_bad_request_result
        )

    def _retrieve_all_lib_tracks_mixin(self, uuid: UUID):
        return self.api_client.get(
            path=reverse('all-library-tracks-detail', kwargs={'pk': uuid}),
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _put_all_lib_tracks_mixin(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('all-library-tracks-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _delete_all_lib_tracks_mixin(self, uuid: UUID):
        return self.api_client.delete(path=reverse('all-library-tracks-detail', kwargs={'pk': uuid}))
