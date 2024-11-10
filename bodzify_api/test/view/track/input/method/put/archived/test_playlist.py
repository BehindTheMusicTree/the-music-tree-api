from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.schema.lib_track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_archived_lib_track_then_manual_playlist_has_plus_1_archived_lib_tracks(self):
        manual_playlist_name = "simple playlist"
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)
        track = self.model_fixture_factory.create_lib_track_with_file(title="not archived 1")
        track.base_playlists.add(manual_playlist)
        track_archived = self.model_fixture_factory.create_lib_track_with_file(title="archived 1", archived=True)
        track_archived.base_playlists.add(manual_playlist)

        response = self._put_lib_track(lib_track_uuid=track.uuid, data_dict={PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        manual_playlist_base_saved: ManualPlaylist = ManualPlaylist.objects.get(user=self.test_user1,
                                                                                name=manual_playlist_name)
        assert manual_playlist_base_saved.library_tracks_archived_count == 2
        assert manual_playlist_base_saved.library_tracks_count == 0

    def test_archived_lib_track_then_criteria_playlist_has_plus_1_archived_lib_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="rock")
        self.model_fixture_factory.create_lib_track_with_file(title="not archived 1", genre=criteria)
        self.model_fixture_factory.create_lib_track_with_file(title="archived 1", archived=True, genre=criteria)
        track_love = self.model_fixture_factory.create_lib_track_with_file(title="Love", genre=criteria)

        response = self._put_lib_track(lib_track_uuid=track_love.uuid, data_dict={PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.genre
        criteria_playlist_saved: CriteriaPlaylist = self.saved_lib_track.genre.criteria_playlist
        assert criteria_playlist_saved.library_tracks_archived_count == 2
        assert criteria_playlist_saved.library_tracks_count == 0
