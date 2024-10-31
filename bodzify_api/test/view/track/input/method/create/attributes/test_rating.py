
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_not_povided_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == None
