from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.put import Fields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_archived_lib_track_then_all_lib_tracks_mixin_has_plus_1_archived_lib_tracks(self):
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 1")
        self.model_fixture_factory.create_lib_track_with_file(title="archived 1", archived=True)
        track_love = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(uuid=track_love.uuid, **{Fields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        assert self.test_user1.all_lib_tracks_mixin.library_tracks_archived_count == 2
        assert self.test_user1.all_lib_tracks_mixin.library_tracks_count == 0
