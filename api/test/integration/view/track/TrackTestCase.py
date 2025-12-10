from uuid import UUID

from django.urls import reverse

from api.model.track.Track import Track
from api.test.utils.AppTestCase import AppTestCase


class TrackTestCase(AppTestCase[Track]):
    model_class = Track
    saved_object: Track
    is_from_track_test_case: bool = True

    def _post_track(self, **kwargs):
        return self.api_client.post(
            path=reverse('track-list'), data=kwargs, format='multipart', handle_response=self._set_results)

    def _post_track_without_file(self, **kwargs):
        return self.api_client.post(
            path=reverse('track-list'), data=kwargs, handle_response=self._set_results)

    def _delete_track(self, uuid):
        return self.api_client.delete(path=reverse('track-detail', kwargs={'pk': uuid}))

    def _retrieve_track(self, uuid: UUID):
        return self.api_client.get(path=reverse('track-detail', kwargs={'pk': uuid}),
                                   handle_response=self._set_results)

    def _list_tracks(self, **kwargs):
        return self.api_client.get(path=reverse('track-list'), data=kwargs, handle_response=self._set_results)
