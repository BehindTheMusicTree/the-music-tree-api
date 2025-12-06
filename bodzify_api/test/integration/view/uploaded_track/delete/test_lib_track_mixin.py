from rest_framework import status

from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_delete_then_not_in_all_uploaded_tracks_mixin(self):
        title = "test"
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title=title, archived=True)
        self.model_fixture_factory.create_uploaded_track_with_file(title='koko', archived=True)
        assert self.test_user1.all_uploaded_tracks_mixin.uploaded_tracks_archived_count == 2

        response = self._delete_uploaded_track(uploaded_track.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.test_user1.all_uploaded_tracks_mixin.uploaded_tracks_archived_count == 1
