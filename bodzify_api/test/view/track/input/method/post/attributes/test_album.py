from rest_framework import status

from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_not_povided_then_none(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None
