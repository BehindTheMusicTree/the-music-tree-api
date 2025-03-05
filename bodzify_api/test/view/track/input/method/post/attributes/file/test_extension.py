from rest_framework import status

from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_wav(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_mp3(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_flac(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
