from rest_framework import status

from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@
class TextCase(LibTrackTestCase):

    def test_id3v1_short_mp3_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_SHORT_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_long_mp3_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_LONG_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_short_flac_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_SHORT_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_long_flac_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_LONG_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_short_wav_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_SHORT_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_long_wav_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_LONG_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_short_mp3_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_SHORT_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_long_mp3_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_LONG_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_short_flac_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_SHORT_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_long_flac_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_LONG_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_short_wav_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_SHORT_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_long_wav_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_LONG_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_riff_short_wav_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_RIFF_SHORT_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_riff_long_wav_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_RIFF_LONG_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_vorbis_short_flac_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_VORBIS_SHORT_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_vorbis_long_flac_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_VORBIS_SHORT_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
