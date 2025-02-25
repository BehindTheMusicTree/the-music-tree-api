import pytest
from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import \
    CriteriaPlaylist
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_create_then_in_first_position_of_genre_playlist_and_other_tracks_after(self):
        genre = self.model_fixture_factory.create_genre(name="Rock")
        lib_track1 = self.model_fixture_factory.create_lib_track_with_file(
            title="We're All To Blame", genre=genre, use_manager_for_genre_playlist_adding=True)
        lib_track2 = self.model_fixture_factory.create_lib_track_with_file(
            title="We're All To lol", genre=genre, use_manager_for_genre_playlist_adding=True)

        response = self._post_lib_track_with_generic_sample_no_tags()

        assert response.status_code == status.HTTP_201_CREATED

        genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=genre)

        assert genre_playlist.lib_track_playlist_rels.get(lib_track=self.saved_object).position == 1
        assert genre_playlist.lib_track_playlist_rels.get(lib_track=lib_track1).position == 2
        assert genre_playlist.lib_track_playlist_rels.get(lib_track=lib_track2).position == 3
