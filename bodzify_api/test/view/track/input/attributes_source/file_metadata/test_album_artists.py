from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.input.attributes_source.file_metadata.StrMetadataFromFileTestCase import (
    StrMetadataFromFileTestCase
)


class TestCase(StrMetadataFromFileTestCase):
    file_extension: str

    def test_none_then_none(self):
        response = \
            self._post_lib_track(TestLibTrackFilename.ALBUM_KOKO_ID3V2_MP3, extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.album_artists.count() == 0

    def test_longest_id3v2_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_MP3, extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED

        expected_name = 'a' * settings.ARTIST_NAME_LEN_MAX
        album = self.saved_object.album
        assert album
        assert album.name == expected_name

    def test_longest_riff_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_RIFF_WAV, extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED

        expected_name = 'a' * settings.ARTIST_NAME_LEN_MAX
        album = self.saved_object.album
        assert album
        assert album.name == expected_name
