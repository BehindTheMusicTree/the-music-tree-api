from uuid import UUID
from pathlib import Path

from django.urls import reverse

from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.test.utils.uploaded_track.UploadedTrackDownloadTestUrl import UploadedTrackDownloadTestUrl
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields
from bodzify_api.utils import data_transformer


class UploadedTrackTestCase(AppTestCase[UploadedTrack]):
    model_class = UploadedTrack
    saved_object: UploadedTrack
    is_from_uploaded_track_test_case: bool = True  # Override the default value from AppTestCase

    TEST_FILES_BASE_DIR = Path(__file__).parent.parent.parent / 'utils' / 'uploaded_track' / 'files'

    def _post_uploaded_track_from_url(
            self, test_uploaded_track_url: UploadedTrackDownloadTestUrl = UploadedTrackDownloadTestUrl.MP3, **kwargs):
        kwargs[Fields.TRACK_FILE_PUBLIC] = str(test_uploaded_track_url)
        return self.api_client.post(
            path=reverse('uploaded-track-list'), data=kwargs, handle_response=self._set_results)

    def _post_uploaded_track(self, test_uploaded_track_filename: UploadedTrackTestFilename, **kwargs):
        file_abs_path = self.TEST_FILES_BASE_DIR / test_uploaded_track_filename

        with open(file_abs_path, "rb") as sample_file:
            file_field_dict = {Fields.TRACK_FILE_PUBLIC: sample_file}
            if kwargs:
                kwargs = data_transformer.merge_two_dicts(file_field_dict, kwargs)
            else:
                kwargs = file_field_dict

            return self.api_client.post(
                path=reverse('uploaded-track-list'), data=kwargs, format='multipart', handle_response=self._set_results)

    def _post_uploaded_track_without_file(self, **kwargs):
        return self.api_client.post(
            path=reverse('uploaded-track-list'), data=kwargs, handle_response=self._set_results)

    def _download_uploaded_track(self, uuid):
        return self.api_client.get(path=reverse('uploaded-track-download', kwargs={'pk': uuid}))

    def _delete_uploaded_track(self, uuid):
        return self.api_client.delete(path=reverse('uploaded-track-detail', kwargs={'pk': uuid}))

    def _retrieve_uploaded_track(self, uuid: UUID):
        return self.api_client.get(path=reverse('uploaded-track-detail', kwargs={'pk': uuid}),
                                   handle_response=self._set_results)

    def _list_uploaded_tracks(self, **kwargs):
        return self.api_client.get(path=reverse('uploaded-track-list'), data=kwargs, handle_response=self._set_results)
