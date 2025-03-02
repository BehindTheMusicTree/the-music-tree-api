from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_none_then_generated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title

    def test_longest_from_id3v1_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == 'a' * settings.LIB_TRACK_TITLE_LEN_MAX

    def test_longest_from_id3v2_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == 'a' * settings.LIB_TRACK_TITLE_LEN_MAX

    def test_longest_from_riff_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_RIFF_WAV)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == 'a' * settings.LIB_TRACK_TITLE_LEN_MAX

    def test_longest_from_vorbis_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_VORBIS_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == 'a' * settings.LIB_TRACK_TITLE_LEN_MAX
