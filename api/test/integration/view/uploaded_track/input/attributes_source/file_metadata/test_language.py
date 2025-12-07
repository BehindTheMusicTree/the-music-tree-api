from rest_framework import status

from api import settings
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_none_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.ALBUM_KOKO_ID3V2_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.album_artists.count() == 0

    def test_long_id3v2_then_truncated(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language
        assert len(self.saved_object.language) == settings.LANGUAGE_LEN_MAX
        assert self.saved_object.language == 'a' * settings.LANGUAGE_LEN_MAX

    def test_long_vorbis_then_truncated(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language
        assert len(self.saved_object.language) == settings.LANGUAGE_LEN_MAX
        assert self.saved_object.language == 'a' * settings.LANGUAGE_LEN_MAX
