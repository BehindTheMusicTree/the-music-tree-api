from rest_framework import status

from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_wav(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert str(round(self.saved_object.track_file.size_in_mo, 2)) == str(
            self.LibTrackGenericSamplesTagsNoneSizeInMo.WAV)

    def test_mp3(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert str(round(self.saved_object.track_file.size_in_mo, 2)) == str(
            self.LibTrackGenericSamplesTagsNoneSizeInMo.MP3)

    def test_flac(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert str(round(self.saved_object.track_file.size_in_mo, 2)) == str(
            self.LibTrackGenericSamplesTagsNoneSizeInMo.FLAC)
