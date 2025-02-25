from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import \
    CriteriaPlaylist
from bodzify_api.serializer.model.lib_track.input.put.Fields import \
    Fields as PutFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_new_criteria_then_decrease_positions_of_following_tracks_in_old_criteria(self):
        old_genre = self.model_fixture_factory.create_genre(name="Metal")
        lib_track_following2 = self.model_fixture_factory.create_lib_track_with_file(
            title="Lodwdw", genre=old_genre, use_manager_for_genre_playlist_adding=True)
        lib_track_following1 = self.model_fixture_factory.create_lib_track_with_file(
            title="cdss", genre=old_genre, use_manager_for_genre_playlist_adding=True)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", genre=old_genre, use_manager_for_genre_playlist_adding=True)

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: "Rock"})

        assert response.status_code == status.HTTP_200_OK
        old_genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria=old_genre)
        assert old_genre_playlist.lib_track_playlist_rels.get(lib_track=lib_track_following1).position == 1
        assert old_genre_playlist.lib_track_playlist_rels.get(lib_track=lib_track_following2).position == 2
