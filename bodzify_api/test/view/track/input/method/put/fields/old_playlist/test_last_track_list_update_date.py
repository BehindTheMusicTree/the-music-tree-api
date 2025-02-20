import pytest

from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.lib_track.input.put.Fields import Fields as PutFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TestCase(LibTrackTestCase):
    def test_track_not_linked_to_genre_anymore_then_update_genre_playlist_last_track_list_update_date(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", genre=genre, use_manager_for_genre_playlist_adding=True)
        criteria_playlist_before_update: CriteriaPlaylist = genre.criteria_playlist

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: ''})

        assert response.status_code == status.HTTP_200_OK
        criteria_playlist_after_update: CriteriaPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user1, uuid=genre.criteria_playlist.uuid)
        assert criteria_playlist_after_update.last_track_list_update_date > \
            criteria_playlist_before_update.last_track_list_update_date

    def test_track_not_linked_to_genre_anymore_then_update_genre_parents_playlist_last_track_list_update_date(self):
        genre_parent = self.model_fixture_factory.create_genre(name='rock')
        genre = self.model_fixture_factory.create_genre(name='rock hard', parent=genre_parent)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", genre=genre, use_manager_for_genre_playlist_adding=True)
        parent_criteria_playlist_before_update: CriteriaPlaylist = genre_parent.criteria_playlist

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: ''})

        assert response.status_code == status.HTTP_200_OK
        genre_parent.refresh_from_db()
        parent_criteria_playlist_after_update: CriteriaPlaylist = genre_parent.criteria_playlist
        assert parent_criteria_playlist_after_update.last_track_list_update_date > \
            parent_criteria_playlist_before_update.last_track_list_update_date

    def test_linked_to_genre_then_update_genreless_playlist_last_track_list_update_date(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", use_manager_for_genre_playlist_adding=True)
        genre = self.model_fixture_factory.create_genre(name='rock')
        criteria_playlist_before_update: CriteriaPlaylist = genre.criteria_playlist

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: genre.name})

        assert response.status_code == status.HTTP_200_OK
        criteria_playlist_after_update: CriteriaPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user1, uuid=genre.criteria_playlist.uuid)
        assert criteria_playlist_after_update.last_track_list_update_date < \
            criteria_playlist_before_update.last_track_list_update_date
