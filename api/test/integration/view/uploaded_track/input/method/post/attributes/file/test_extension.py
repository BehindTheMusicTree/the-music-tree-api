from rest_framework import status

from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_wav(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_mp3(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_flac(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
