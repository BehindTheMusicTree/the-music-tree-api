from rest_framework import status

from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_create_then_in_first_position_of_genre_playlist_and_other_tracks_after(self):
        genre = self.model_fixture_factory.create_genre(name="Rock")
        uploaded_track_added_first = self.model_fixture_factory.create_uploaded_track_with_file(
            title="We're All To Blame", genre=genre, use_manager_for_genre_playlist_adding=True)
        uploaded_track_added_second = self.model_fixture_factory.create_uploaded_track_with_file(
            title="We're All To lol", genre=genre, use_manager_for_genre_playlist_adding=True)

        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        playlist_tracks_by_positions = genre.criteria_playlist.uploaded_tracks_not_archived_dict_by_position
        assert playlist_tracks_by_positions[1] == uploaded_track_added_second
        assert playlist_tracks_by_positions[2] == uploaded_track_added_first
