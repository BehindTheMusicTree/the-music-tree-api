import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, cast

from ddf import G, N
from django_dynamic_fixture import global_settings
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import get_user_model

from bodzify_api.model.album.Album import Album
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import Fields as CriteriaFields
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.model.criteria.children.tag.Tag import Tag
from bodzify_api.model.musicbrainz_resource.children.artist.MusicbrainzArtist import MusicbrainzArtist
from bodzify_api.model.musicbrainz_resource.children.artist.Fields import Fields as MusicbrainzArtistFields
from bodzify_api.model.musicbrainz_resource.children.recording.MusicbrainzRecording import MusicbrainzRecording
from bodzify_api.model.musicbrainz_resource.children.recording.MusicbrainzRecording \
    import Fields as MusicbrainzRecordingFields
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.Fields import Fields as BasePlaylistFields
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.lib.Fields import Fields as LibraryTrackFields
from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.model.track.file.TrackFile import Fields as TrackFileFields
from bodzify_api.model.user.User import User

global_settings.DDF_FIELD_FIXTURES['django.db.models.fields.generated.GeneratedField'] = lambda: None  # type: ignore


class ModelFixtureFactory:
    default_test_user: 'User'
    lib_samples_dir: Path
    generic_sample_path: Path

    def __init__(self, default_test_user: 'User', lib_samples_dir: Path, generic_sample_path: Path) -> None:
        self.default_test_user = default_test_user
        self.lib_samples_dir = lib_samples_dir
        self.generic_sample_path = generic_sample_path

    @staticmethod
    def create_user(username=None, email=None, password='password123', **kwargs) -> 'User':
        UserModel = get_user_model()
        unique_id = str(uuid.uuid4())[:8]
        user = N(UserModel,
                 username=username or f'testuser_{unique_id}',
                 email=email or f'testuser_{unique_id}@example.com',
                 is_test_user=True,
                 **kwargs)
        user.set_password(password)
        user.save()
        return cast('User', user)

    def __create_criteria(self,
                          name: str,
                          model_class: type[Criteria],
                          user: Optional[User] = None, **kwargs) -> Criteria:
        model_fields = {
            CriteriaFields.CREATED_ON: timezone.make_aware(datetime.now()),
            CriteriaFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            CriteriaFields.USER: user or self.default_test_user,
            CriteriaFields.NAME: name,
            CriteriaFields.PARENT: None,
        }
        model_fields.update(kwargs)
        return model_class.objects.create(**model_fields)

    def _create_file(self, user: User, lib_track: LibraryTrack, filename: Optional[str], **kwargs) -> TrackFile:

        if not os.path.exists(user.lib_abs_path):
            os.makedirs(user.lib_abs_path)

        file_path = self.lib_samples_dir / filename if filename else self.generic_sample_path

        track_file_path_in_lib = user.lib_abs_path / os.path.basename(file_path)
        shutil.copy(file_path, track_file_path_in_lib)

        model_fields = {
            TrackFileFields.CREATED_ON: timezone.make_aware(datetime.now()),
            TrackFileFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            TrackFileFields.USER: user,
            TrackFileFields.LIB_TRACK: lib_track,
            TrackFileFields.FILE: str(track_file_path_in_lib)
        }
        model_fields.update(kwargs)
        return G(TrackFile, **model_fields)

    def _create_lib_track(self, user: User, title: str, **kwargs) -> LibraryTrack:
        model_fields = {
            LibraryTrackFields.CREATED_ON: timezone.make_aware(datetime.now()),
            LibraryTrackFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            LibraryTrackFields.USER: user,
            LibraryTrackFields.TITLE: title,
            LibraryTrackFields.ARTISTS: [],
            LibraryTrackFields.ALBUM: None,
            LibraryTrackFields.POSITION_IN_ALBUM: None,
            LibraryTrackFields.GENRE: None,
            LibraryTrackFields.RATING: None,
            LibraryTrackFields.LANGUAGE: None,
            LibraryTrackFields.PLAY_COUNT: 0,
            LibraryTrackFields.ARCHIVED: False
        }
        model_fields.update(kwargs)
        library_track = G(LibraryTrack, **model_fields)

        if kwargs.get(LibraryTrackFields.ARTISTS):
            library_track.artists.set(kwargs[LibraryTrackFields.ARTISTS])

        return library_track

    def create_lib_track_with_file(self,
                                   title: str,
                                   filename: Optional[str] = None,
                                   user: Optional[User] = None,
                                   **kwargs) -> LibraryTrack:
        user = user or self.default_test_user
        with transaction.atomic():
            library_track = self._create_lib_track(user=user, title=title, **kwargs)
            self._create_file(user=user, lib_track=library_track, filename=filename)

        return library_track

    def create_artist(self, name: str, user: Optional[User] = None, **kwargs) -> Artist:
        model_fields = {
            ArtistFields.CREATED_ON: timezone.make_aware(datetime.now()),
            ArtistFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            ArtistFields.USER: user or self.default_test_user,
            ArtistFields.NAME: name
        }
        model_fields.update(kwargs)
        return G(Artist, **model_fields)

    def create_album(self, name: str, user: Optional[User] = None, **kwargs) -> Album:
        model_fields = {
            AlbumFields.CREATED_ON: timezone.make_aware(datetime.now()),
            AlbumFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            AlbumFields.USER: user or self.default_test_user,
            AlbumFields.ALBUM_ARTISTS: [],
            AlbumFields.YEAR: None,
            AlbumFields.NAME: name
        }
        model_fields.update(kwargs)
        return G(Album, **model_fields)

    def create_genre(self, name: str, **kwargs) -> Criteria:
        return self.__create_criteria(name=name, model_class=Genre, **kwargs)

    def create_tag(self, name: str, **kwargs) -> Criteria:
        return self.__create_criteria(name=name, model_class=Tag, **kwargs)

    def create_manual_playlist(self, name: str, user: Optional[User] = None, **kwargs) -> ManualPlaylist:
        base_playlist_model_fields = {
            BasePlaylistFields.CREATED_ON: timezone.make_aware(datetime.now()),
            BasePlaylistFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            BasePlaylistFields.USER: user or self.default_test_user,
            BasePlaylistFields.PLAY_COUNT: 0
        }
        base_playlist_model_fields.update(kwargs)

        base_playlist = G(BasePlaylist, **base_playlist_model_fields)

        return G(ManualPlaylist, base_playlist=base_playlist, name=name)

    def create_musicbrainz_recording(self, musicbrainz_id: str, title: str, **kwargs) -> MusicbrainzRecording:
        model_fields = {
            MusicbrainzRecordingFields.CREATED_ON: timezone.make_aware(datetime.now()),
            MusicbrainzRecordingFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            MusicbrainzRecordingFields.MUSICBRAINZ_ARTISTS: None,
            MusicbrainzRecordingFields.SCORE: 1.0,
            MusicbrainzRecordingFields.DURATION_IN_SEC: 200,
            MusicbrainzRecordingFields.RELEASE_DATE: None,
            MusicbrainzRecordingFields.MUSICBRAINZ_ID: musicbrainz_id,
            MusicbrainzRecordingFields.TITLE: title
        }
        model_fields.update(kwargs)
        return G(MusicbrainzRecording, **model_fields)

    def create_musicbrainz_artist(self, musicbrainz_id: str, name: str, **kwargs) -> MusicbrainzArtist:
        model_fields = {
            MusicbrainzArtistFields.CREATED_ON: timezone.make_aware(datetime.now()),
            MusicbrainzArtistFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            MusicbrainzArtistFields.MUSICBRAINZ_ID: musicbrainz_id,
            MusicbrainzArtistFields.NAME: name
        }
        model_fields.update(kwargs)
        return G(MusicbrainzArtist, **model_fields)
