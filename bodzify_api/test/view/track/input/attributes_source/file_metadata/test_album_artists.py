from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):
    file_extension: str

    def test_none_then_none(self):
        response = \
            self._post_lib_track(TestLibTrackFilename.ALBUM_KOKO_ID3V2_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.album_artists.count() == 0

    def test_longest_id3v2_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_MP3)
        assert response.status_code == status.HTTP_201_CREATED

        assert self.saved_object.album
        assert len(self.saved_object.album.name) == settings.ALBUM_NAME_LEN_MAX
        assert self.saved_object.album.name == 'a' * settings.ALBUM_NAME_LEN_MAX

    def test_longest_riff_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_RIFF_WAV)
        assert response.status_code == status.HTTP_201_CREATED

        assert self.saved_object.album
        assert len(self.saved_object.album.name) == settings.ALBUM_NAME_LEN_MAX
        assert self.saved_object.album.name == 'a' * settings.ALBUM_NAME_LEN_MAX

    def test_longest_vorbis_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_VORBIS_FLAC)
        assert response.status_code == status.HTTP_201_CREATED

        assert self.saved_object.album
        assert len(self.saved_object.album.name) == settings.ALBUM_NAME_LEN_MAX
        assert self.saved_object.album.name == 'a' * settings.ALBUM_NAME_LEN_MAX
