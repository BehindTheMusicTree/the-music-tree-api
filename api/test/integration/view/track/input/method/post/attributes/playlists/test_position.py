from rest_framework import status

from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_create_then_in_first_position_of_genre_playlist_and_other_tracks_after(self):
        genre = self.model_fixture_factory.create_genre(name="Rock")
        track_added_first = self.model_fixture_factory.create_track_with_file(
            title="We're All To Blame", genre=genre, use_manager_for_genre_playlist_adding=True)
        track_added_second = self.model_fixture_factory.create_track_with_file(
            title="We're All To lol", genre=genre, use_manager_for_genre_playlist_adding=True)

        response = self._post_track()

        assert response.status_code == status.HTTP_201_CREATED
        playlist_tracks_by_positions = genre.criteria_playlist.tracks_not_archived_dict_by_position
        assert playlist_tracks_by_positions[1] == track_added_second
        assert playlist_tracks_by_positions[2] == track_added_first
