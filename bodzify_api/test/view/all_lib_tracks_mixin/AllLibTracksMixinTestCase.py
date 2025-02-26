from uuid import UUID

from django.urls import reverse

from bodzify_api.model.all_lib_tracks_mixin.AllLibTracksMixin import AllLibTracksMixin
from bodzify_api.test.ApiTestCase import ApiTestCase


class AllLibTracksMixinTestCase(ApiTestCase[AllLibTracksMixin]):
    def _post_all_lib_tracks_mixin(self, **kwargs):
        return self.api_client.post(
            path=reverse('all-library-tracks-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _get_all_lib_tracks_mixin(self, **kwargs):
        return self.api_client.get(
            path=reverse('all-library-tracks-list'),
            data=kwargs,
            handle_response=self._set_results
        )

    def _retrieve_all_lib_tracks_mixin(self, uuid: UUID):
        return self.api_client.get(
            path=reverse('all-library-tracks-detail', kwargs={'pk': uuid}),
            handle_response=self._set_results
        )

    def _put_all_lib_tracks_mixin(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('all-library-tracks-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _delete_all_lib_tracks_mixin(self, uuid: UUID):
        return self.api_client.delete(path=reverse('all-library-tracks-detail', kwargs={'pk': uuid}))
