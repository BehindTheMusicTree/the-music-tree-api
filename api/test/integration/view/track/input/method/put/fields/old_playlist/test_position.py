from rest_framework import status

from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.serializer.model.track.input.put.Fields import Fields as PutFields
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_new_criteria_then_decrease_positions_of_following_tracks_in_old_criteria(self):
        old_genre = self.model_fixture_factory.create_genre(name="Metal")
        track_following2 = self.model_fixture_factory.create_track_with_file(
            title="Lodwdw", genre=old_genre, use_manager_for_genre_playlist_adding=True)
        track_following1 = self.model_fixture_factory.create_track_with_file(
            title="cdss", genre=old_genre, use_manager_for_genre_playlist_adding=True)
        track = self.model_fixture_factory.create_track_with_file(
            title="Love", genre=old_genre, use_manager_for_genre_playlist_adding=True)
        old_genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria=old_genre)
        assert old_genre_playlist.track_playlist_rels.get(track=track).position == 1
        assert old_genre_playlist.track_playlist_rels.get(
            track=track_following1).position == 2
        assert old_genre_playlist.track_playlist_rels.get(
            track=track_following2).position == 3

        response = self._put_track(track.uuid, **{PutFields.GENRE: "Rock"})

        assert response.status_code == status.HTTP_200_OK
        old_genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria=old_genre)
        assert old_genre_playlist.track_playlist_rels.get(
            track=track_following1).position == 1
        assert old_genre_playlist.track_playlist_rels.get(
            track=track_following2).position == 2
