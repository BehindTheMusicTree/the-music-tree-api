from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_none_then_none(self):
        response = self._post_lib_track(TestLibTrackFilename.ALBUM_KOKO_ID3V2_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 0

    def test_long_id3v2_then_truncated(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_MAX_A_ID3V2_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language
        assert len(self.saved_object.language) == settings.LANGUAGE_LEN_MAX
        assert self.saved_object.language == 'a' * settings.LANGUAGE_LEN_MAX
