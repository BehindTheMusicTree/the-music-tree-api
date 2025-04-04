from rest_framework import status

from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


"""
Small files are handled differently by Django. They are stored in memory instead of being written to disk.
Thus the python file object is not available. This test case is to ensure that the API handles this case.
"""


class TestCase(LibTrackTestCase):

    def test_in_memory_then_ok(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3)
        assert response.status_code == status.HTTP_201_CREATED
