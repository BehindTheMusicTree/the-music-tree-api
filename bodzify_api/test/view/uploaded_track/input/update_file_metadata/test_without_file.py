from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_without_a_file_and_a_title_then_ok(self):
        track = self.model_fixture_factory.create_uploaded_track_with_file(title="Foire")
        response = self._put_uploaded_track(uuid=track.uuid, **{PostFields.TITLE: "Jobo"})
        assert response.status_code == status.HTTP_200_OK
