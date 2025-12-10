from rest_framework import status

from api.serializer.model.track.input.Fields import Fields
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_archived_track_then_all_tracks_mixin_has_plus_1_archived_tracks(self):
        self.model_fixture_factory.create_track_with_file(title="not archived 1")
        self.model_fixture_factory.create_track_with_file(title="archived 1", archived=True)
        track_love = self.model_fixture_factory.create_track_with_file(title="Love")

        response = self._put_track(uuid=track_love.uuid, **{Fields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        assert self.test_user1.all_tracks_mixin.tracks_archived_count == 2
        assert self.test_user1.all_tracks_mixin.tracks_not_archived_count == 1
