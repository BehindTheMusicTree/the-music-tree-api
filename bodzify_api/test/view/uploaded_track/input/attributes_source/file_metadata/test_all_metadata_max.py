from rest_framework import status

from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class TextCase(LibTrackTestCase):

    def test_id3v1_SMALL_MP3_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_long_mp3_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_BIG_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_short_flac_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_long_flac_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_BIG_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_short_wav_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v1_long_wav_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_BIG_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_SMALL_MP3_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_long_mp3_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_BIG_MP3)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_short_flac_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_long_flac_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_BIG_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_short_wav_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_id3v2_long_wav_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_BIG_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_riff_short_wav_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_riff_long_wav_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_RIFF_BIG_WAV)
        assert response.status_code == status.HTTP_201_CREATED

    def test_vorbis_short_flac_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

    def test_vorbis_long_flac_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
