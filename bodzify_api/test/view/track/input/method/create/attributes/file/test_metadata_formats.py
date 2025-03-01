import pytest
from rest_framework import status

from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TextCase(LibTrackTestCase):

    def test_id3v1_mp3_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_flac_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_wav_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V1_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_mp3_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_flac_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_wav_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_riff_wav_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_RIFF_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_vorbis_flac_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_VORBIS_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
