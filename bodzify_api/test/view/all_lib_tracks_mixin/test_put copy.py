from uuid import UUID
from bodzify_api.test.view.all_lib_tracks_mixin.AllLibTracksMixinTestCase import AllLibTracksMixinTestCase


class TestCase(AllLibTracksMixinTestCase):

    def test_put_then_error(self):
        response = self._put_all_lib_track_mixin(uuid=UUID('00000000-0000-0000-0000-000000000000'))
        assert response.status_code == 404
