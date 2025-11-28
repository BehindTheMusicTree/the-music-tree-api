from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_none_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.ALBUM_KOKO_ID3V2_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert not self.saved_object.genre

    def test_long_id3v2_then_truncated(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert len(self.saved_object.genre.name) == settings.CRITERIA_NAME_LEN_MAX
        assert self.saved_object.genre.name == 'a' * settings.CRITERIA_NAME_LEN_MAX

    def test_long_riff_then_truncated(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert len(self.saved_object.genre.name) == settings.CRITERIA_NAME_LEN_MAX
        assert self.saved_object.genre.name == 'a' * settings.CRITERIA_NAME_LEN_MAX

    def test_long_vorbis_then_truncated(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert len(self.saved_object.genre.name) == settings.CRITERIA_NAME_LEN_MAX
        assert self.saved_object.genre.name == 'a' * settings.CRITERIA_NAME_LEN_MAX
