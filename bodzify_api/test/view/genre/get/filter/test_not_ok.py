from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_filter_not_existing_then_error(self):
        response = self._get_lib_tracks(sdkfhsdkjfhskjfh='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
