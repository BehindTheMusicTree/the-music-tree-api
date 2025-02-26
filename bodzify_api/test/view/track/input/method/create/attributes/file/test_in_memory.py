from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


"""
Small files are handled differently by Django. They are stored in memory instead of being written to disk.
Thus the python file object is not available. This test case is to ensure that the API handles this case.
"""


class TestCase(LibTrackTestCase):

    def test_in_memory_then_ok(self):
        response = self._post_lib_track_with_specific_sample("in_memory.flac")
        assert response.status_code == status.HTTP_201_CREATED
