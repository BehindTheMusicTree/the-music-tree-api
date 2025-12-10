from rest_framework import status

from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_delete_then_not_in_all_tracks_mixin(self):
        title = "test"
        track = self.model_fixture_factory.create_track_with_file(title=title, archived=True)
        self.model_fixture_factory.create_track_with_file(title='koko', archived=True)
        assert self.test_user1.all_tracks_mixin.tracks_archived_count == 2

        response = self._delete_track(track.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.test_user1.all_tracks_mixin.tracks_archived_count == 1
