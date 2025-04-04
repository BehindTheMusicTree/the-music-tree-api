from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.input.put.Fields import Fields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_archived_uploaded_track_then_all_uploaded_tracks_mixin_has_plus_1_archived_uploaded_tracks(self):
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 1")
        self.model_fixture_factory.create_uploaded_track_with_file(title="archived 1", archived=True)
        track_love = self.model_fixture_factory.create_uploaded_track_with_file(title="Love")

        response = self._put_uploaded_track(uuid=track_love.uuid, **{Fields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        assert self.test_user1.all_uploaded_tracks_mixin.uploaded_tracks_archived_count == 2
        assert self.test_user1.all_uploaded_tracks_mixin.uploaded_tracks_not_archived_count == 1
