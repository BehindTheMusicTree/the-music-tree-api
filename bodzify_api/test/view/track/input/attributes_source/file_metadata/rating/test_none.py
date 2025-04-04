from rest_framework import status

from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_mp3_then_none(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None

    def test_wav_then_none(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None

    def test_flac_then_none(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None
