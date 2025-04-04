from uuid import UUID

from django.urls import reverse

from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.test.utils.uploaded_track.UploadedTrackDownloadTestUrl import LibTracTestkUrl
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields


class LibTrackTestCase(AppTestCase[UploadedTrack]):
    model_class = UploadedTrack
    saved_object: UploadedTrack
    is_from_uploaded_track_test_case: bool = True  # Override the default value from AppTestCase

    def _post_uploaded_track_from_url(self, test_uploaded_track_url: LibTracTestkUrl = LibTracTestkUrl.MP3, **kwargs):
        kwargs[Fields.TRACK_FILE_PUBLIC] = str(test_uploaded_track_url)
        return self.api_client.post(
            path=reverse('library-track-list'), data=kwargs, handle_response=self._set_results)

    def _post_uploaded_track_without_file(self, **kwargs):
        return self.api_client.post(
            path=reverse('library-track-list'), data=kwargs, handle_response=self._set_results)

    def _download_uploaded_track(self, uuid):
        return self.api_client.get(path=reverse('library-track-download', kwargs={'pk': uuid}))

    def _delete_uploaded_track(self, uuid):
        return self.api_client.delete(path=reverse('library-track-detail', kwargs={'pk': uuid}))

    def _retrieve_uploaded_track(self, uuid: UUID):
        return self.api_client.get(path=reverse('library-track-detail', kwargs={'pk': uuid}),
                                   handle_response=self._set_results)

    def _list_uploaded_tracks(self, **kwargs):
        return self.api_client.get(path=reverse('library-track-list'), data=kwargs, handle_response=self._set_results)
