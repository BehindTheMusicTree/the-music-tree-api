from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_long_then_renamed(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FILENAME_151_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.filename == \
            UploadedTrackTestFilename.FILENAME_151_MP3[-settings.UPLOADED_TRACK_FILENAME_LEN_MAX:]

    def test_same_filename_so_suffixe_added(self):
        self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3)
        track1 = self.saved_object

        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3)
        track2 = self.saved_object

        assert response.status_code == status.HTTP_201_CREATED
        assert track1.track_file
        assert track1.track_file.filename == UploadedTrackTestFilename.METADATA_NONE_MP3
        assert track2.track_file.filename.startswith(UploadedTrackTestFilename.METADATA_NONE_MP3[:-4])
        assert track2.track_file.filename.endswith('.mp3')
