import os

from rest_framework import status

from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.musicbrainz_resource.children.recording.MbRecording import MusicbrainzRecording
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.user.User import User
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.user.UserTestCase import UserTestCase


class TestCase(UserTestCase):
    saved_object: User
    model_class = User

    def test_delete_then_ok(self):
        user = self.model_fixture_factory.create_user('jojo')

        self._login_as_test_admin()
        response = self._delete_user(user.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_then_lib_dir_removed(self):
        user = self.model_fixture_factory.create_user()
        self.model_fixture_factory.create_lib_track_with_file(user=user, title='Dr mo')
        assert os.path.exists(user.lib_abs_path)

        self._login_as_test_admin()
        response = self._delete_user(user.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not os.path.exists(user.lib_abs_path)

    def test_delete_then_criteria_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        criteria_name = 'Rock'
        self.model_fixture_factory.create_genre(user=user, name=criteria_name)
        assert Criteria.objects.filter(user=user, name=criteria_name).count() == 1

        self._login_as_test_admin()
        response = self._delete_user(user.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Criteria.objects.filter(user=user, name=criteria_name).count() == 0

    def test_delete_then_playlist_removed(self):
        user = self.model_fixture_factory.create_user()
        assert CriteriaPlaylist.objects.filter(user=user, type=CriteriaTypePks.GENRE, criteria=None).count() == 1
        self._login_as_user(user)

        self._login_as_test_admin()
        response = self._delete_user(user.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert CriteriaPlaylist.objects.filter(user=user, type=CriteriaTypePks.GENRE).count() == 0

    def test_delete_then_lib_track_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        title = 'Dr mo'
        self.model_fixture_factory.create_lib_track_with_file(user=user, title=title)
        assert LibraryTrack.objects.filter(user=user, title=title).count() == 1

        self._login_as_test_admin()
        response = self._delete_user(user.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(user=user, title=title).count() == 0

    def test_delete_then_album_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        album_name = 'Skyfall'
        album = self.model_fixture_factory.create_album(user=user, name=album_name)
        self.model_fixture_factory.create_lib_track_with_file(user=user, title='Skyfall', album=album)

        assert Album.objects.filter(user=user, name=album_name).count() == 1

        self._login_as_test_admin()
        response = self._delete_user(user.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(user=user, name=album_name).count() == 0

    def test_delete_then_artist_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        artist_name = 'Adele'
        artist = self.model_fixture_factory.create_artist(name=artist_name, user=user)

        self.model_fixture_factory.create_lib_track_with_file(user=user, title='Skyfall', artists=[artist])

        assert Artist.objects.filter(user=user, name=artist_name).count() == 1

        self._login_as_test_admin()
        response = self._delete_user(user.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Artist.objects.filter(user=user, name=artist_name).count() == 0

    def test_delete_then_musicbrainz_recording_not_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        mb_recording_title = "Drown (Massano remix)"
        mb_recording = self.model_fixture_factory.create_musicbrainz_recording(
            musicbrainz_id="4a45b00b-273d-40ed-9ecd-42f387f59c22",
            title=mb_recording_title,
            musicbrainz_artists=[])
        track = self.model_fixture_factory.create_lib_track_with_file(
            user=user, title='Drown',
            test_lib_track_filename=TestLibTrackFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3)
        track.track_file.musicbrainz_recording = mb_recording
        track.track_file.save()

        assert MusicbrainzRecording.objects.filter(title=mb_recording_title).exists()

        self._login_as_test_admin()
        response = self._delete_user(user.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert MusicbrainzRecording.objects.filter(musicbrainz_id="4a45b00b-273d-40ed-9ecd-42f387f59c22").count() == 1
