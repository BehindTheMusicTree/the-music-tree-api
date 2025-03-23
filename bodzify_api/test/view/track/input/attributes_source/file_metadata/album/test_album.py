from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_none_then_none(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album is None

    def test_long_id3v2_then_truncated(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert len(self.saved_object.album.name) == settings.ALBUM_NAME_LEN_MAX
        assert self.saved_object.album.name == 'a' * settings.ALBUM_NAME_LEN_MAX

    def test_long_riff_then_truncated(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert len(self.saved_object.album.name) == settings.ALBUM_NAME_LEN_MAX
        assert self.saved_object.album.name == 'a' * settings.ALBUM_NAME_LEN_MAX

    def test_long_vorbis_then_truncated(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert len(self.saved_object.album.name) == settings.ALBUM_NAME_LEN_MAX
        assert self.saved_object.album.name == 'a' * settings.ALBUM_NAME_LEN_MAX

    def test_max_id3v1_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == 'a' * settings.ALBUM_NAME_LEN_MAX_ID3V1
