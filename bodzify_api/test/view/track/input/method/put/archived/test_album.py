
from rest_framework import status

from bodzify_api.serializer.schema.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_archived_lib_track_then_album_has_plus_1_archived_lib_tracks(self):
        album = self.model_fixture_factory.create_album(name="Jojo")
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 1", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 2", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 3", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="archived 1", album=album, archived=True)
        track_love = self.model_fixture_factory.create_lib_track_with_file(title="Love", album=album)
        data = {PutFields.ARCHIVED: "true"}
        response = self._put_lib_track(lib_track_uuid=track_love.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.album and self.saved_lib_track.album.library_tracks_archived_count == 2

    def test_unarchived_then_album_has_minus_1_archived_lib_tracks(self):
        album = self.model_fixture_factory.create_album(name="Jojo")
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 1", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 2", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 3", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="archived 1", album=album, archived=True)
        track = self.model_fixture_factory.create_lib_track_with_file(title="Love", album=album, archived=True)
        data = {PutFields.ARCHIVED: "false"}
        response = self._put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.album and self.saved_lib_track.album.library_tracks_archived_count == 1
