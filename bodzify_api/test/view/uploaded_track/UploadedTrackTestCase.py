from pathlib import Path

from django.urls import reverse

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as LibTrackPostFields
from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.utils import data_transformer


class UploadedTrackTestCase(AppTestCase[LibraryTrack]):
    model_class = LibraryTrack
    saved_object: LibraryTrack

    TEST_FILES_BASE_DIR = Path(__file__).parent.parent.parent / 'utils' / 'uploaded_track' / 'files'

    def _post_uploaded_track(self, test_uploaded_track_filename: UploadedTrackTestFilename, **kwargs):
        file_abs_path = self.TEST_FILES_BASE_DIR / test_uploaded_track_filename

        with open(file_abs_path, "rb") as sample_file:
            file_field_dict = {LibTrackPostFields.TRACK_FILE_PUBLIC: sample_file}
            if kwargs:
                kwargs = data_transformer.merge_two_dicts(file_field_dict, kwargs)
            else:
                kwargs = file_field_dict

            return self.api_client.post(
                path=reverse('library-track-list'), data=kwargs, format='multipart', handle_response=self._set_results)

