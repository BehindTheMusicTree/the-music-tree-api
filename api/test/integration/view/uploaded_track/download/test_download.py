from rest_framework import status

from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_ok(self):
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="We're All To Blame")

        response = self._download_uploaded_track(uuid=uploaded_track.uuid)

        assert response.status_code == status.HTTP_200_OK
