from uuid import UUID

from rest_framework import status

from .AllLibTracksMixinTestCase import AllLibTracksMixinTestCase


class TestCase(AllLibTracksMixinTestCase):

    def test_delete_then_error(self):
        response = self._delete_all_lib_tracks_mixin(uuid=UUID('00000000-0000-0000-0000-000000000000'))
        assert response.status_code == status.HTTP_404_NOT_FOUND
