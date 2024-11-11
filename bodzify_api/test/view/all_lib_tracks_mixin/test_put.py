from uuid import UUID

from rest_framework import status

from .AllLibTracksMixinTestCase import AllLibTracksMixinTestCase


class TestCase(AllLibTracksMixinTestCase):

    def test_put_then_error(self):
        response = self._put_all_lib_tracks_mixin(uuid=UUID('00000000-0000-0000-0000-000000000000'))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
