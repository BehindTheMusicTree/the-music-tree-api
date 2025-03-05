from pathlib import Path

from rest_framework import status

from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_in_library(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert Path(self.saved_object.track_file.file.name) == \
            Path(self.test_user1.lib_path_relative_to_media) / TestLibTrackFilename.METADATA_NONE_MP3
        assert self.test_user1.does_track_filename_exist_in_lib(TestLibTrackFilename.METADATA_NONE_MP3)
