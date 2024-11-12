from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_extra_field_then_error(self):
        response = self._extract_default_mine_track(kwargs={"field_not_handled": "pofkefposkfwp"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
