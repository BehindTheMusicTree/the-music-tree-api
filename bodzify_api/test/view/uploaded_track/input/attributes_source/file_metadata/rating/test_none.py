from rest_framework import status

from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_mp3_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None

    def test_wav_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None

    def test_flac_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None
