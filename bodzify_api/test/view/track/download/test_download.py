from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_ok(self):
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="We're All To Blame")

        response = self._download_uploaded_track(uuid=uploaded_track.uuid)

        assert response.status_code == status.HTTP_200_OK
