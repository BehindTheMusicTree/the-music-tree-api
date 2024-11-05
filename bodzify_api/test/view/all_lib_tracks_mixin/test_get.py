from rest_framework import status

from .AllLibTracksMixinTestCase import AllLibTracksMixinTestCase


class TestCase(AllLibTracksMixinTestCase):

    def test_get_then_one_result(self):
        response = self._get_all_lib_track_mixin()
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
