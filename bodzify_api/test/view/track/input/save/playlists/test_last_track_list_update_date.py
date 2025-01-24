import pytest

from rest_framework import status

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.lib_track.input.put import Fields as PutFields
from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as LibTrackPostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TestCase(LibTrackTestCase):
    def test_track_newly_linked_to_genre_then_update_genre_playlist_last_track_list_update_date(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        criteria_playlist: CriteriaPlaylist = genre.criteria_playlist
        genre_playlist_last_track_list_update_date_before_update = criteria_playlist.last_track_list_update_date
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", use_manager_for_genre_playlist_adding=True)

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: genre.name})

        assert response.status_code == status.HTTP_200_OK
        genre.refresh_from_db()
        criteria_playlist: CriteriaPlaylist = genre.criteria_playlist
        assert criteria_playlist.last_track_list_update_date > genre_playlist_last_track_list_update_date_before_update

    def test_track_newly_linked_to_genre_then_update_genre_parent_playlist_last_track_list_update_date(self):
        genre_parent = self.model_fixture_factory.create_genre(name='rock')
        genre = self.model_fixture_factory.create_genre(name='rock hard', parent=genre_parent)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", use_manager_for_genre_playlist_adding=True)

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: genre.name})

        assert response.status_code == status.HTTP_200_OK
        genre_parent.refresh_from_db()
        parent_criteria_playlist: CriteriaPlaylist = genre_parent.criteria_playlist
        assert genre.criteria_playlist.last_track_list_update_date < parent_criteria_playlist.last_track_list_update_date

    def test_track_newly_linked_to_no_genre_then_update_genreless_playlist_last_track_list_update_date(self):
        genreless_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1,
                                                                            type=CriteriaTypePks.GENRE,
                                                                            criteria=None)

        genre = self.model_fixture_factory.create_genre(name='rock')
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", genre=genre)

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: ''})
        assert response.status_code == status.HTTP_200_OK
        genreless_playlist.refresh_from_db()
        assert genreless_playlist.last_track_list_update_date > genreless_playlist.last_track_list_update_date
