
import os
import pytest
from rest_framework import status

from bodzify_api import settings
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.album.Album import Album
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesPks
from bodzify_api.model.musicbrainz.recording.MusicbrainzRecording import MusicbrainzRecording
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.track.input.endpoint.post import Fields as TrackPostFields
from bodzify_api.test.view.user.UserViewTestCase import UserViewTestCase
from bodzify_api.utils import musicbrainz


class TestCase(UserViewTestCase):

    def test_delete_then_ok(self):
        user = self.model_fixture_factory.create_user('jojo')
        response = self._login_as_test_admin_and_delete_user(user.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_then_lib_dir_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        self._post_lib_track_with_generic_sample_no_tags()
        user_lib_abs_path = settings.LIBRARIES_DIR / (settings.USER_LIBRARIES_DIR_NAME_PREFIXE + str(user.pk))
        assert os.path.exists(user_lib_abs_path)
        response = self._login_as_test_admin_and_delete_user(user.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not os.path.exists(user_lib_abs_path)

    def test_delete_then_criteria_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        criteria_name = 'Rock'
        data = {TrackPostFields.GENRE_NAME: criteria_name}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert Criteria.objects.filter(user=user, name=criteria_name).count() == 1
        assert response.status_code == status.HTTP_201_CREATED
        response = self._login_as_test_admin_and_delete_user(user.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Criteria.objects.filter(user=user, name=criteria_name).count() == 0

    @pytest.mark.usefixtures("enable_audio_metadata_analysis")
    def test_delete_then_musicbrainz_recording_not_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        response = self._post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert MusicbrainzRecording.objects.filter(musicbrainz_id="4a45b00b-273d-40ed-9ecd-42f387f59c22").count() == 1
        response = self._login_as_test_admin_and_delete_user(user.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert MusicbrainzRecording.objects.filter(musicbrainz_id="4a45b00b-273d-40ed-9ecd-42f387f59c22").count() == 1

    def test_delete_then_playlist_removed(self):
        user = self.model_fixture_factory.create_user()
        assert CriteriaPlaylist.objects.filter(user=user, type=CriteriaTypesPks.GENRE, criteria=None).count() == 1
        self._login_as_user(user)
        response = self._login_as_test_admin_and_delete_user(user.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert CriteriaPlaylist.objects.filter(user=user, type=CriteriaTypesPks.GENRE).count() == 0

    def test_delete_then_lib_track_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        title = 'Dr mo'
        data = {TrackPostFields.TITLE: title}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert LibraryTrack.objects.filter(user=user, title=title).count() == 1
        assert response.status_code == status.HTTP_201_CREATED
        response = self._login_as_test_admin_and_delete_user(user.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(user=user, title=title).count() == 0

    def test_delete_then_album_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        album_name = 'Skyfall'
        data = {TrackPostFields.ALBUM_NAME: album_name}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert Album.objects.filter(user=user, name=album_name).count() == 1
        assert response.status_code == status.HTTP_201_CREATED
        response = self._login_as_test_admin_and_delete_user(user.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(user=user, name=album_name).count() == 0

    def test_delete_then_artist_removed(self):
        user = self.model_fixture_factory.create_user()
        self._login_as_user(user)
        artist_name = 'Adele'
        data = {TrackPostFields.ARTISTS_NAMES: artist_name}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Artist.objects.filter(user=user, name=artist_name).count() == 1
        response = self._login_as_test_admin_and_delete_user(user.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Artist.objects.filter(user=user, name=artist_name).count() == 0
