from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_none_then_none(self):
        response = self._post_lib_track(TestLibTrackFilename.ALBUM_KOKO_ID3V2_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert not self.saved_object.genre

    def test_long_id3v2_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert len(self.saved_object.genre.name) == settings.CRITERIA_NAME_LEN_MAX
        assert self.saved_object.genre.name == 'a' * settings.CRITERIA_NAME_LEN_MAX

    def test_long_riff_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_RIFF_WAV)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert len(self.saved_object.genre.name) == settings.CRITERIA_NAME_LEN_MAX
        assert self.saved_object.genre.name == 'a' * settings.CRITERIA_NAME_LEN_MAX

    def test_long_vorbis_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_VORBIS_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert len(self.saved_object.genre.name) == settings.CRITERIA_NAME_LEN_MAX
        assert self.saved_object.genre.name == 'a' * settings.CRITERIA_NAME_LEN_MAX

    def test_id3v1_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert len(self.saved_object.genre.name) == settings.CRITERIA_NAME_LEN_MAX
        assert self.saved_object.genre.name == 'a' * settings.CRITERIA_NAME_LEN_MAX
