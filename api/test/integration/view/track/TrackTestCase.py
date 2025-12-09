from uuid import UUID

from django.urls import reverse

from api.model.track.Track import Track
from api.test.utils.AppTestCase import AppTestCase
from api.test.utils.track.TrackDownloadTestUrl import TrackDownloadTestUrl
from api.test.utils.track.TrackTestFilename import TrackTestFilename
from api.serializer.model.track.input.post.Fields import Fields
from api.utils import data_transformer


class TrackTestCase(AppTestCase[Track]):
    model_class = Track
    saved_object: Track
    is_from_track_test_case: bool = True

    def _post_track_from_url(
            self, test_track_url: TrackDownloadTestUrl = TrackDownloadTestUrl.MP3, **kwargs):
        kwargs[Fields.TRACK_FILE_PUBLIC] = str(test_track_url)
        return self.api_client.post(
            path=reverse('uploaded-track-list'), data=kwargs, handle_response=self._set_results)

    def _post_track(
            self, test_track_filename: TrackTestFilename = TrackTestFilename.METADATA_NONE_MP3,
            **kwargs):
        file_abs_path = self.TEST_FILES_BASE_DIR / test_track_filename.value

        with open(file_abs_path, "rb") as sample_file:
            file_field_dict = {Fields.TRACK_FILE_PUBLIC: sample_file}
            if kwargs:
                kwargs = data_transformer.merge_two_dicts(file_field_dict, kwargs)
            else:
                kwargs = file_field_dict

            return self.api_client.post(
                path=reverse('uploaded-track-list'), data=kwargs, format='multipart', handle_response=self._set_results)

    def _post_track_without_file(self, **kwargs):
        return self.api_client.post(
            path=reverse('uploaded-track-list'), data=kwargs, handle_response=self._set_results)

    def _download_track(self, uuid):
        return self.api_client.get(path=reverse('uploaded-track-download', kwargs={'pk': uuid}))

    def _delete_track(self, uuid):
        return self.api_client.delete(path=reverse('uploaded-track-detail', kwargs={'pk': uuid}))

    def _retrieve_track(self, uuid: UUID):
        return self.api_client.get(path=reverse('uploaded-track-detail', kwargs={'pk': uuid}),
                                   handle_response=self._set_results)

    def _list_tracks(self, **kwargs):
        return self.api_client.get(path=reverse('uploaded-track-list'), data=kwargs, handle_response=self._set_results)
