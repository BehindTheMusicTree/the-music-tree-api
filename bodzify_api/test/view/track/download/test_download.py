from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_ok(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            filename="sample.mp3", title="We're All To Blame")
        response = self._download_lib_track(uuid=lib_track.uuid)
        assert response.status_code == status.HTTP_200_OK
