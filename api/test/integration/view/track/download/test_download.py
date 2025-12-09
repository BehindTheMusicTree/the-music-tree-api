from rest_framework import status

from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_ok(self):
        track = self.model_fixture_factory.create_track_with_file(title="We're All To Blame")

        response = self._download_track(uuid=track.uuid)

        assert response.status_code == status.HTTP_200_OK
