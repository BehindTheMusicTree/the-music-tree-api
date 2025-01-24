from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.put import Fields as PutFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_archived_lib_track_then_criteria_has_plus_1_archived_lib_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="Jojo")
        self.model_fixture_factory.create_lib_track_with_file(
            title="not archived 1", genre=criteria)
        self.model_fixture_factory.create_lib_track_with_file(
            title="not archived 2", genre=criteria)
        self.model_fixture_factory.create_lib_track_with_file(
            title="not archived 3", genre=criteria)
        self.model_fixture_factory.create_lib_track_with_file(
            title="archived 1", genre=criteria, archived=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="archived 2", genre=criteria, archived=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="archived 3", genre=criteria, archived=True)
        track_love = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", genre=criteria)
        data = {PutFields.ARCHIVED: "true"}
        response = self._put_lib_track(uuid=track_love.uuid, **data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.genre and self.saved_lib_track.genre.library_tracks_archived_count == 4

    def test_unarchived_then_criteria_has_minus_1_archived_lib_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="Jojo")
        self.model_fixture_factory.create_lib_track_with_file(
            title="not archived 1", genre=criteria)
        self.model_fixture_factory.create_lib_track_with_file(
            title="not archived 2", genre=criteria)
        self.model_fixture_factory.create_lib_track_with_file(
            title="not archived 3", genre=criteria)
        self.model_fixture_factory.create_lib_track_with_file(
            title="archived 1", genre=criteria, archived=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="archived 2", genre=criteria, archived=True)
        track = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", genre=criteria, archived=True)
        data = {PutFields.ARCHIVED: "false"}
        response = self._put_lib_track(uuid=track.uuid, **data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.genre and self.saved_lib_track.genre.library_tracks_archived_count == 2
