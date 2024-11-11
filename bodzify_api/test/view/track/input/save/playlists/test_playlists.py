import pytest
from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.lib_track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_new_genre_then_in_new_genre_playlist(self):
        genre_name = "Rock"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(lib_track.uuid, data_dict={PutFields.GENRE_NAME: genre_name})

        assert response.status_code == status.HTTP_200_OK
        track_playlists = self.saved_lib_track.playlists.all()
        assert len(track_playlists) == 2
        criteria_playlists = CriteriaPlaylist.objects.filter(user=self.test_user1, playlist__in=track_playlists)
        assert criteria_playlists.filter(criteria__name=genre_name).exists()

    def test_existing_genre_then_track_in_existing_playlist(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(lib_track.uuid, data_dict={PutFields.GENRE_NAME: genre_name})
        assert response.status_code == status.HTTP_200_OK

        track_playlists = self.saved_lib_track.playlists.all()
        assert len(track_playlists) == 2

        genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=genre)
        assert lib_track in genre_playlist.library_tracks.all()

    def test_existing_genre_with_2_successive_ascendants_then_track_in_3_existing_playlists(self):
        rock_genre_name = "Rock"
        hardrock_genre_name = "Hard rock"
        emo_genre_name = "Emo"

        rock_genre = self.model_fixture_factory.create_genre(name=rock_genre_name)
        hardrock_genre = self.model_fixture_factory.create_genre(name=hardrock_genre_name, parent=rock_genre)
        self.model_fixture_factory.create_genre(name=emo_genre_name, parent=hardrock_genre)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(lib_track.uuid, data_dict={PutFields.GENRE_NAME: emo_genre_name})

        assert response.status_code == status.HTTP_200_OK
        lib_track_playlists = self.saved_lib_track.playlists.all()
        assert len(lib_track_playlists) == 4

        lib_track_criteria_playlists = CriteriaPlaylist.objects.filter(user=self.test_user1,
                                                                       playlist__in=lib_track_playlists)
        assert lib_track_criteria_playlists.filter(criteria__name=emo_genre_name).exists()
        assert lib_track_criteria_playlists.filter(criteria__name=hardrock_genre_name).exists()
        assert lib_track_criteria_playlists.filter(criteria__name=rock_genre_name).exists()
