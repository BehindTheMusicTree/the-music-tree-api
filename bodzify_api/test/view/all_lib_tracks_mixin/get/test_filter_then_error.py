from rest_framework import status

from ..AllLibTracksMixinTestCase import AllLibTracksMixinTestCase


class TestCase(AllLibTracksMixinTestCase):

    def test_filter_then_error(self):
        response = self._get_all_lib_tracks_mixin(kwargs={'title': 'a'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
