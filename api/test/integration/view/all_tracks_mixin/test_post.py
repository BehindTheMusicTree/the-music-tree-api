from rest_framework import status

from api.test.integration.view.all_tracks_mixin.AllTracksMixinTestCase import AllTracksMixinTestCase


class TestCase(AllTracksMixinTestCase):

    def test_post_then_not_allowed(self):
        response = self._post_all_tracks_mixin()
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
