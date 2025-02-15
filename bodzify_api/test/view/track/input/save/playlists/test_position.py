import pytest

from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_new_genre_then_first_position(self):
        genre_name = "Rock"
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.GENRE_NAME: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria__name=genre_name)
        assert genre_playlist.lib_track_playlist_rels.get(lib_track=self.saved_lib_track).position == 1

    def test_existing_then_ok_genre_then_first_position_and_other_tracks_after(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        lib_track1 = self.model_fixture_factory.create_lib_track_with_file(
            title="We're All To Blame", genre=genre, use_manager_for_genre_playlist_adding=True)
        lib_track2 = self.model_fixture_factory.create_lib_track_with_file(
            title="We're All To Blame", genre=genre, use_manager_for_genre_playlist_adding=True)

        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.GENRE_NAME: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria__name=genre_name)
        assert genre_playlist.lib_track_playlist_rels.get(lib_track=self.saved_lib_track).position == 1
        assert genre_playlist.lib_track_playlist_rels.get(lib_track=lib_track1).position == 3
        assert genre_playlist.lib_track_playlist_rels.get(lib_track=lib_track2).position == 2
