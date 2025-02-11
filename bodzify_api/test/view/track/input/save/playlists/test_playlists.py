import pytest

from rest_framework import status

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.lib_track.input.put import Fields as PutFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_newly_created_genre_then_in_new_genre_playlist(self):
        genre_name = "Rock"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: genre_name})

        assert response.status_code == status.HTTP_200_OK
        track_playlists_uuids_list = [playlist.uuid for playlist in self.saved_lib_track.playlists.all()]
        assert len(track_playlists_uuids_list) == 1
        rock_criteria_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=genre_name)
        assert rock_criteria_playlist.playlist.uuid in track_playlists_uuids_list

    def test_existing_genre_then_track_in_existing_playlist(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: genre_name})
        assert response.status_code == status.HTTP_200_OK

        track_playlists_uuids_list = [playlist.uuid for playlist in self.saved_lib_track.playlists.all()]
        assert len(track_playlists_uuids_list) == 1

        rock_criteria_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=genre_name)
        assert rock_criteria_playlist.playlist.uuid in track_playlists_uuids_list

    def test_existing_genre_with_2_successive_ascendants_then_track_in_3_existing_playlists(self):
        genre_rock_name = "Rock"
        hardgenre_rock_name = "Hard rock"
        emo_genre_name = "Emo"

        genre_rock = self.model_fixture_factory.create_genre(name=genre_rock_name)
        hardgenre_rock = self.model_fixture_factory.create_genre(name=hardgenre_rock_name, parent=genre_rock)
        self.model_fixture_factory.create_genre(name=emo_genre_name, parent=hardgenre_rock)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: emo_genre_name})

        assert response.status_code == status.HTTP_200_OK
        lib_track_playlists = self.saved_lib_track.playlists.all()
        assert len(lib_track_playlists) == 4

        lib_track_criteria_playlists = CriteriaPlaylist.objects.filter(user=self.test_user1,
                                                                       playlist__in=lib_track_playlists)
        assert lib_track_criteria_playlists.filter(criteria__name=emo_genre_name).exists()
        assert lib_track_criteria_playlists.filter(criteria__name=hardgenre_rock_name).exists()
        assert lib_track_criteria_playlists.filter(criteria__name=genre_rock_name).exists()
