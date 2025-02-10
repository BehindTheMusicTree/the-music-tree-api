import pytest

from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_delete_then_update_genre_playlist_last_track_update_date(self) -> None:
        genre = self.model_fixture_factory.create_genre(name='rock')
        track = self.model_fixture_factory.create_lib_track_with_file(
            title="We're All To Blame", genre=genre, use_manager_for_genre_playlist_adding=True)
        genre_playlist_last_track_list_update_date_before_deletion = genre.criteria_playlist.last_track_list_update_date

        response = self._delete_lib_track(uuid=track.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        genre.criteria_playlist.refresh_from_db()
        assert genre.criteria_playlist.last_track_list_update_date > \
            genre_playlist_last_track_list_update_date_before_deletion

    def test_delete_then_update_parent_of_parent_of_genre_playlist_last_track_update_date(self) -> None:
        genre1 = self.model_fixture_factory.create_genre(name='rock')
        genre2 = self.model_fixture_factory.create_genre(name='punk', parent=genre1)
        genre3 = self.model_fixture_factory.create_genre(name='punk hardcore', parent=genre2)
        track = self.model_fixture_factory.create_lib_track_with_file(
            title="We're All To Blame", genre=genre3, use_manager_for_genre_playlist_adding=True)
        genre1_playlist_last_track_list_update_date_before_deletion = \
            genre1.criteria_playlist.last_track_list_update_date

        response = self._delete_lib_track(uuid=track.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        genre1.criteria_playlist.refresh_from_db()
        assert genre1.criteria_playlist.last_track_list_update_date > \
            genre1_playlist_last_track_list_update_date_before_deletion
