from pathlib import Path

from rest_framework import status

from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_in_library(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert Path(self.saved_object.track_file.file.name) == \
            Path(self.test_user1.lib_path_relative_to_media) / UploadedTrackTestFilename.METADATA_NONE_MP3
        assert self.test_user1.does_track_filename_exist_in_lib(UploadedTrackTestFilename.METADATA_NONE_MP3)
