from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_none_then_generated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title

    def test_from_id3v1_big_file_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_ID3V1_SMALL_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert len(self.saved_object.title) == settings.LIB_TRACK_TITLE_LEN_MAX_ID3V1
        assert self.saved_object.title == 'a' * settings.LIB_TRACK_TITLE_LEN_MAX_ID3V1

    def test_long_from_id3v2_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_ID3V2_SMALL_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert len(self.saved_object.title) == settings.LIB_TRACK_TITLE_LEN_MAX
        assert self.saved_object.title == 'a' * settings.LIB_TRACK_TITLE_LEN_MAX

    def test_long_from_riff_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_RIFF_SMALL_WAV)

        assert response.status_code == status.HTTP_201_CREATED
        assert len(self.saved_object.title) == settings.LIB_TRACK_TITLE_LEN_MAX
        assert self.saved_object.title == 'a' * settings.LIB_TRACK_TITLE_LEN_MAX

    def test_long_from_vorbis_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert len(self.saved_object.title) == settings.LIB_TRACK_TITLE_LEN_MAX
        assert self.saved_object.title == 'a' * settings.LIB_TRACK_TITLE_LEN_MAX
