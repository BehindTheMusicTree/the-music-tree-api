from pathlib import Path

from rest_framework import status

from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_in_library(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert Path(self.saved_object.track_file.file.name) == \
            Path(self.test_user1.lib_path_relative_to_media) / LibTrackTestFilename.METADATA_NONE_MP3
        assert self.test_user1.does_track_filename_exist_in_lib(LibTrackTestFilename.METADATA_NONE_MP3)
