from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.input.attributes_source.file_metadata.FieldStrFromFileMetadataTestCase import (
    FieldStrNullableFromFileMetadataTestCase
)


class TestCase(FieldStrNullableFromFileMetadataTestCase):
    file_extension: str

    def test_none_then_none(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, extension=self.file_extension)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None

    def test_longest_then_ok(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3v2_MP3, extension=self.file_extension)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == 'a' * settings.ALBUM_NAME_LEN_MAX
