from uuid import UUID

from rest_framework import status

from .AllUploadedTracksMixinTestCase import AllUploadedTracksMixinTestCase


class TestCase(AllUploadedTracksMixinTestCase):

    def test_delete_then_405(self):
        response = self._delete_all_uploaded_tracks_mixin(uuid=UUID('00000000-0000-0000-0000-000000000000'))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
