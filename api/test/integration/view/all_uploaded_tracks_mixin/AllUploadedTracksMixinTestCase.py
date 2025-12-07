from uuid import UUID

from django.urls import reverse

from api.test.utils.AppTestCase import AppTestCase
from api.model.all_uploaded_tracks_mixin.AllUploadedTracksMixin import AllUploadedTracksMixin


class AllUploadedTracksMixinTestCase(AppTestCase[AllUploadedTracksMixin]):
    def _post_all_uploaded_tracks_mixin(self, **kwargs):
        return self.api_client.post(path=reverse('all-uploaded-tracks-list'),
                                    data=kwargs,
                                    content_type='application/json',
                                    handle_response=self._set_results)

    def _get_all_uploaded_tracks_mixin(self, **kwargs):
        return self.api_client.get(
            path=reverse('all-uploaded-tracks-list'), data=kwargs, handle_response=self._set_results)

    def _retrieve_all_uploaded_tracks_mixin(self, uuid: UUID):
        return self.api_client.get(
            path=reverse('all-uploaded-tracks-detail', kwargs={'pk': uuid}), handle_response=self._set_results)

    def _put_all_uploaded_tracks_mixin(self, uuid: UUID, **kwargs):
        return self.api_client.put(path=reverse('all-uploaded-tracks-detail', kwargs={'pk': uuid}),
                                   data=kwargs,
                                   content_type='application/json',
                                   handle_response=self._set_results)

    def _delete_all_uploaded_tracks_mixin(self, uuid: UUID):
        return self.api_client.delete(path=reverse('all-uploaded-tracks-detail', kwargs={'pk': uuid}))
