from rest_framework import status

from bodzify_api.serializer.schema.lib_track.input.endpoint.put import Fields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_archived_lib_track_then_all_lib_tracks_mixin_has_plus_1_archived_lib_tracks(self):
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 1")
        self.model_fixture_factory.create_lib_track_with_file(title="archived 1", archived=True)
        track_love = self.model_fixture_factory.create_lib_track_with_file(title="Love")
        data = {Fields.ARCHIVED: "true"}
        response = self._put_lib_track(lib_track_uuid=track_love.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.test_user1.all_lib_track_mixin.library_tracks_archived_count == 2
        assert self.test_user1.all_lib_track_mixin.library_tracks_count == 0
