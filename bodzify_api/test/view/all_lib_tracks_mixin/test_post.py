from rest_framework import status

from bodzify_api.test.view.all_uploaded_tracks_mixin.AllUploadedTracksMixinTestCase import AllUploadedTracksMixinTestCase


class TestCase(AllUploadedTracksMixinTestCase):

    def test_post_then_not_allowed(self):
        response = self._post_all_uploaded_tracks_mixin()
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
