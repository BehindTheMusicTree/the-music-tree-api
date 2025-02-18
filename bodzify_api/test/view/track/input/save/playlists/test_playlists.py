import pytest

from rest_framework import status

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
        track_playlists_uuids = [playlist.uuid for playlist in self.saved_object.playlists.all()]
        assert len(track_playlists_uuids) == 1
        rock_criteria_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=genre_name)
        assert rock_criteria_playlist.playlist.uuid in track_playlists_uuids

    def test_existing_then_ok_genre_then_track_in_existing_playlist(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: genre_name})
        assert response.status_code == status.HTTP_200_OK

        track_playlists_uuids = [playlist.uuid for playlist in self.saved_object.playlists.all()]
        assert len(track_playlists_uuids) == 1

        rock_criteria_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=genre_name)
        assert rock_criteria_playlist.playlist.uuid in track_playlists_uuids

    def test_existing_then_ok_genre_with_2_successive_ascendants_then_track_in_3_existing_playlists(self):
        genre_rock_name = "Rock"
        genre_hard_rock_name = "Hard rock"
        genre_emo_name = "Emo"

        genre_rock = self.model_fixture_factory.create_genre(name=genre_rock_name)
        hardgenre_rock = self.model_fixture_factory.create_genre(name=genre_hard_rock_name, parent=genre_rock)
        self.model_fixture_factory.create_genre(name=genre_emo_name, parent=hardgenre_rock)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: genre_emo_name})

        assert response.status_code == status.HTTP_200_OK
        track_playlists_uuids = [playlist.uuid for playlist in self.saved_object.playlists.all()]
        assert len(track_playlists_uuids) == 3

        criteria_rock_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=genre_rock_name)
        assert criteria_rock_playlist.playlist.uuid in track_playlists_uuids

        criteria_hard_rock_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=genre_hard_rock_name)
        assert criteria_hard_rock_playlist.playlist.uuid in track_playlists_uuids

        criteria_emo_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=genre_emo_name)
        assert criteria_emo_playlist.playlist.uuid in track_playlists_uuids
