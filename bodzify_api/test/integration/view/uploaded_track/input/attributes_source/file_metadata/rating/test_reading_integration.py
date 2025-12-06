from rest_framework import status

from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_id3v2_mp3_5_stars_then_10(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RATING_ID3V2_5_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 10

    def test_id3v2_mp3_0_stars_then_0(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RATING_ID3V2_0_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 0

    def test_vorbis_flac_5_stars_then_10(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RATING_VORBIS_5_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 10

    def test_vorbis_flac_0_stars_then_0(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RATING_VORBIS_0_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 0

    def test_riff_wav_5_stars_then_10(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RATING_RIFF_BASE_100_KID3_5_STAR_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 10

    def test_traktor_mp3_5_stars_then_10(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RATING_ID3V2_TRACKTOR_5_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 10

    def test_traktor_flac_5_stars_then_10(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RATING_VORBIS_TRAKTOR_5_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 10



