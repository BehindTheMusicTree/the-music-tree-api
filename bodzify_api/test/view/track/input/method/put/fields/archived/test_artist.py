from rest_framework import status

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.schema.model.lib_track.input.put.put import Fields as PutFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_archived_lib_track_then_artist_has_plus_1_archived_lib_tracks(self):
        artist = self.model_fixture_factory.create_artist(name="Jojo")
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 1", artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 2", artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 3", artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="archived 1", artists=[artist], archived=True)
        track_love = self.model_fixture_factory.create_lib_track_with_file(title="Love", artists=[artist])

        response = self._put_lib_track(uuid=track_love.uuid, **{PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].lib_tracks_archived_count == 2

    def test_unarchived_then_artist_has_minus_1_archived_lib_tracks(self):
        artist = self.model_fixture_factory.create_artist(name="Jojo")
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 1", artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 2", artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 3", artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="archived 1", artists=[artist], archived=True)
        track = self.model_fixture_factory.create_lib_track_with_file(title="Love", artists=[artist], archived=True)

        response = self._put_lib_track(uuid=track.uuid, **{PutFields.ARCHIVED: "false"})

        assert response.status_code == status.HTTP_200_OK
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].lib_tracks_archived_count == 1
