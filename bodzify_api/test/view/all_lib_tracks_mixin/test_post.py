from rest_framework import status

from bodzify_api.test.view.all_lib_tracks_mixin.AllLibTracksMixinTestCase import \
    AllLibTracksMixinTestCase


class TestCase(AllLibTracksMixinTestCase):

    def test_post_then_not_allowed(self):
        response = self._post_all_lib_tracks_mixin()
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
