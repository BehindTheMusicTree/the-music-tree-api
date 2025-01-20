from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_no_field_specified_then_error(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Polo")
        response = self._put_lib_track(uuid=lib_track.uuid)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
