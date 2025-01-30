import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, TypeVar, cast

from ddf import G, N
from django_dynamic_fixture import global_settings
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.files import File

from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as LibTrackPostFields
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
from bodzify_api.model.play.Play import Play
from bodzify_api.model.play.Fields import Fields as PlayFields
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.playlist.children.manual.Fields import Fields as ManualPlaylistFields
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.lib.Fields import Fields as LibraryTrackFields
from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.model.track.file.TrackFile import Fields as TrackFileFields
from bodzify_api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount
from bodzify_api.model.user.User import User
from bodzify_api.view.viewset.model.lib_track.LibTrackCreationType import LibTrackCreationType

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

    T = TypeVar('T', bound='Criteria')

    def __create_criteria(self,
                          name: str,
                          model_class: type[T],
                          user: Optional[User] = None, **kwargs) -> T:
        now = timezone.make_aware(datetime.now())
        model_fields = {
            CriteriaFields.CREATED_ON: kwargs.get(CriteriaFields.CREATED_ON, now),
            CriteriaFields.UPDATED_ON: kwargs.get(CriteriaFields.UPDATED_ON, now),
            CriteriaFields.USER: user or self.default_test_user,
            CriteriaFields.NAME_PUBLIC: name,
            CriteriaFields.PARENT: None,
        }
        model_fields.update(kwargs)
        return model_class.objects.create(**model_fields)

    def _create_file(
            self, user: User, lib_track: LibraryTrack, track_file_path_in_lib: Optional[Path],
            **kwargs) -> TrackFile:
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
        now = timezone.make_aware(datetime.now())
        model_fields = {
            LibraryTrackFields.CREATED_ON: kwargs.get(LibraryTrackFields.CREATED_ON, now),
            LibraryTrackFields.UPDATED_ON: kwargs.get(LibraryTrackFields.UPDATED_ON, now),
            LibraryTrackFields.USER: user,
            LibraryTrackFields.TITLE: title,
        }
        model_fields.update(kwargs)
        library_track = G(LibraryTrack, **model_fields)

        if kwargs.get(LibraryTrackFields.ARTISTS):
            library_track.artists.set(kwargs[LibraryTrackFields.ARTISTS])

        return library_track

    def create_lib_track_with_file(
        self,
        title: str,
        filename: Optional[str] = None,
        user: Optional[User] = None,
        use_manager_for_genre_playlist_adding: bool = False,
        **kwargs
    ) -> LibraryTrack:
        user = user or self.default_test_user

        now = timezone.make_aware(datetime.now())
        model_fields = {
            LibraryTrackFields.CREATED_ON: kwargs.get(LibraryTrackFields.CREATED_ON, now),
            LibraryTrackFields.UPDATED_ON: kwargs.get(LibraryTrackFields.UPDATED_ON, now),
            LibraryTrackFields.USER: user,
            LibraryTrackFields.TITLE: title,
        }
        model_fields.update(kwargs)

        if not os.path.exists(user.lib_abs_path):
            os.makedirs(user.lib_abs_path)
        file_path = self.lib_samples_dir / filename if filename else self.generic_sample_path
        track_file_path_in_lib = user.lib_abs_path / os.path.basename(file_path)
        shutil.copy(file_path, track_file_path_in_lib)

        if use_manager_for_genre_playlist_adding:
            with open(track_file_path_in_lib, 'rb') as f:
                django_file = File(f, name=os.path.basename(track_file_path_in_lib))
                model_fields.update({LibraryTrackFields.TRACK_FILE_PUBLIC: django_file})
                if LibraryTrackFields.GENRE in model_fields:
                    genre: Genre = model_fields[LibraryTrackFields.GENRE]
                    model_fields[LibTrackPostFields.GENRE_UUID] = genre.uuid
                    model_fields.pop(LibraryTrackFields.GENRE)
                library_track = LibraryTrack.objects.create(**model_fields, creation_type=LibTrackCreationType.POST)
        else:
            with transaction.atomic():
                library_track = self._create_lib_track(user=user, title=title, **kwargs)
                self._create_file(user=user, lib_track=library_track, track_file_path_in_lib=track_file_path_in_lib)

        return library_track

    def create_play(self, content_object: TrackablePlayCount, **kwargs) -> Play:
        model_fields = {PlayFields.CREATED_ON: timezone.make_aware(datetime.now()),
                        PlayFields.UPDATED_ON: timezone.make_aware(datetime.now()),
                        PlayFields.CONTENT_OBJECT: content_object}
        model_fields.update(kwargs)
        return G(Play, **model_fields)

    def create_artist(self, name: str, user: Optional[User] = None, **kwargs) -> Artist:
        model_fields = {
            ArtistFields.CREATED_ON: timezone.make_aware(datetime.now()),
            ArtistFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            ArtistFields.USER: user or self.default_test_user,
            ArtistFields.NAME_INTERNAL: name
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
            AlbumFields.NAME_INTERNAL: name
        }
        model_fields.update(kwargs)
        return G(Album, **model_fields)

    def create_genre(self, name: str, **kwargs) -> Genre:
        return self.__create_criteria(name=name, model_class=Genre, **kwargs)

    def create_tag(self, name: str, **kwargs) -> Tag:
        return self.__create_criteria(name=name, model_class=Tag, **kwargs)

    def create_manual_playlist(self, name: str, user: Optional[User] = None, **kwargs) -> ManualPlaylist:
        now = timezone.make_aware(datetime.now())
        model_fields = {
            # Base Playlist fields
            PlaylistFields.CREATED_ON: kwargs.get(PlaylistFields.CREATED_ON, now),
            PlaylistFields.UPDATED_ON: kwargs.get(PlaylistFields.UPDATED_ON, now),
            PlaylistFields.USER: user or self.default_test_user,
            PlaylistFields.PLAY_COUNT: kwargs.get(PlaylistFields.PLAY_COUNT, 0),
            PlaylistFields.LAST_TRACK_LIST_UPDATE_DATE: kwargs.get(PlaylistFields.LAST_TRACK_LIST_UPDATE_DATE, now),
            # ManualPlaylist specific field
            ManualPlaylistFields.NAME_PUBLIC: name,  # Maps to _name in the model
        }

        with transaction.atomic():
            # Let Django's ORM handle the inheritance. G() doesn't handle inheritance well.
            manual_playlist = ManualPlaylist.objects.create(**model_fields)
            return manual_playlist

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
