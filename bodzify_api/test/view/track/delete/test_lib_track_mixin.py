from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_delete_then_not_in_all_lib_tracks_mixin(self):
        title = "test"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title=title, archived=True)
        self.model_fixture_factory.create_lib_track_with_file(title='koko', archived=True)
        assert self.test_user1.all_lib_tracks_mixin.library_tracks_archived_count == 2

        response = self._delete_lib_track(lib_track.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.test_user1.all_lib_tracks_mixin.library_tracks_archived_count == 1
