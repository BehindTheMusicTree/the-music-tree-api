import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import TypeVar, cast

from ddf import G, N
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import transaction
from django.utils import timezone
from django_dynamic_fixture import global_settings

from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.model.criteria.children.tag.Tag import Tag
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import Fields as CriteriaFields
from bodzify_api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import UploadedTrackPlaylistRel
from bodzify_api.model.uploaded_track_playlist_rel.Fields import Fields as UploadedTrackPlaylistRelFields
from bodzify_api.model.musicbrainz_resource.children.artist.Fields import Fields as MusicbrainzArtistFields
from bodzify_api.model.musicbrainz_resource.children.artist.MbArtist import MbArtist
from bodzify_api.model.musicbrainz_resource.children.recording.MbRecording import Fields as MusicbrainzRecordingFields
from bodzify_api.model.musicbrainz_resource.children.recording.MbRecording import MusicbrainzRecording
from bodzify_api.model.play.Fields import Fields as PlayFields
from bodzify_api.model.play.Play import Play
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.manual.Fields import Fields as ManualPlayListFields
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.playlist.Fields import Fields as PlayListFields
from bodzify_api.model.uploaded_track.file.TrackFile import Fields as TrackFileFields
from bodzify_api.model.uploaded_track.file.TrackFile import TrackFile
from bodzify_api.model.uploaded_track.Fields import Fields as UploadedTrackFields
from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount
from bodzify_api.model.user.User import User
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from bodzify_api.model.spotify_resource.children.track.Fields import Fields as TrackFields
from bodzify_api.model.spotify_resource.children.artist.Fields import Fields as ArtistFields
from bodzify_api.model.artist.Fields import Fields as ArtistModelFields
from bodzify_api.model.album.Fields import Fields as AlbumModelFields


global_settings.DDF_FIELD_FIXTURES['django.db.models.fields.generated.GeneratedField'] = lambda: None  # type: ignore


class ModelFixtureFactory:
    default_test_user: 'User'
    test_uploaded_track_dir: Path

    def __init__(self, default_test_user: 'User', test_uploaded_track_dir: Path) -> None:
        self.default_test_user = default_test_user
        self.test_uploaded_track_dir = test_uploaded_track_dir

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

    def __create_criteria(self, name: str, model_class: type[T], user: User | None = None, **kwargs) -> T:
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
            self, user: User, uploaded_track: UploadedTrack, track_file_path_in_lib: Path | None, **kwargs) -> TrackFile:
        model_fields = {
            TrackFileFields.CREATED_ON: timezone.make_aware(datetime.now()),
            TrackFileFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            TrackFileFields.USER: user,
            TrackFileFields.UPLOADED_TRACK: uploaded_track,
            TrackFileFields.FILE: str(track_file_path_in_lib)
        }
        model_fields.update(kwargs)
        return G(TrackFile, **model_fields)

    def _create_uploaded_track(self, user: User, title: str | None = None, **kwargs) -> UploadedTrack:
        now = timezone.make_aware(datetime.now())
        model_fields = {
            UploadedTrackFields.CREATED_ON: kwargs.get(UploadedTrackFields.CREATED_ON, now),
            UploadedTrackFields.UPDATED_ON: kwargs.get(UploadedTrackFields.UPDATED_ON, now),
            UploadedTrackFields.USER: user,
            UploadedTrackFields.TITLE: title or "Untitled",
        }
        model_fields.update(kwargs)
        uploaded_track = G(UploadedTrack, **model_fields)

        if kwargs.get(UploadedTrackFields.ARTISTS):
            uploaded_track.artists.set(kwargs[UploadedTrackFields.ARTISTS])

        return uploaded_track

    def create_uploaded_track_playlist_rel(
            self, playlist: Playlist, uploaded_track: UploadedTrack, user: User | None = None,) -> UploadedTrackPlaylistRel:
        model_fields = {
            UploadedTrackPlaylistRelFields.USER: user or self.default_test_user,
            UploadedTrackPlaylistRelFields.PLAYLIST: playlist,
            UploadedTrackPlaylistRelFields.UPLOADED_TRACK_INTERNAL: uploaded_track,
        }
        return G(UploadedTrackPlaylistRel, **model_fields)

    def create_uploaded_track_with_file(
        self,
        title: str | None = "test",
        test_uploaded_track_filename: UploadedTrackTestFilename | None = UploadedTrackTestFilename.DEFAULT_MP3,
        user: User | None = None,
        use_manager_for_genre_playlist_adding: bool = False,
        **kwargs
    ) -> UploadedTrack:
        user = user or self.default_test_user

        now = timezone.make_aware(datetime.now())
        model_fields = {
            UploadedTrackFields.CREATED_ON: kwargs.get(UploadedTrackFields.CREATED_ON, now),
            UploadedTrackFields.UPDATED_ON: kwargs.get(UploadedTrackFields.UPDATED_ON, now),
            UploadedTrackFields.USER: user,
            UploadedTrackFields.TITLE: title,
        }
        model_fields.update(kwargs)

        if not os.path.exists(user.lib_abs_path):
            os.makedirs(user.lib_abs_path)

        filename_str = test_uploaded_track_filename.value if test_uploaded_track_filename else None
        file_path = self.test_uploaded_track_dir / filename_str
        track_file_path_in_lib = user.lib_abs_path / filename_str
        try:
            shutil.copy(file_path, track_file_path_in_lib)
        except OSError as e:
            if e.errno == 28:
                stat = shutil.disk_usage(user.lib_abs_path)
                raise OSError(
                    f"No space left on device. Disk usage: {stat.used / (1024**3):.2f}GB used, "
                    f"{stat.free / (1024**3):.2f}GB free out of {stat.total / (1024**3):.2f}GB total. "
                    f"Please free up disk space to continue tests."
                ) from e
            raise

        if use_manager_for_genre_playlist_adding:
            with open(track_file_path_in_lib, 'rb') as f:
                django_file = File(f, name=str(track_file_path_in_lib))
                model_fields.update({UploadedTrackFields.TRACK_FILE_INTERNAL: django_file})
                uploaded_track = UploadedTrack.objects.create(**model_fields)
        else:
            with transaction.atomic():
                uploaded_track = self._create_uploaded_track(user=user, title=title, **kwargs)
                self._create_file(user=user, uploaded_track=uploaded_track,
                                  track_file_path_in_lib=track_file_path_in_lib)

        return uploaded_track

    def create_play(self, content: TrackablePlayCount, user: User | None = None, **kwargs) -> Play:
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(content)

        model_fields = {
            PlayFields.USER: user or self.default_test_user,
            PlayFields.CREATED_ON: timezone.make_aware(datetime.now()),
            PlayFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            PlayFields.CONTENT_TYPE: content_type,
            PlayFields.CONTENT: content.pk
        }
        model_fields.update(kwargs)
        return G(Play, **model_fields)

    def create_artist(self, name: str, user: User | None = None, **kwargs) -> Artist:
        model_fields = {
            ArtistModelFields.CREATED_ON: timezone.make_aware(datetime.now()),
            ArtistModelFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            ArtistModelFields.USER: user or self.default_test_user,
            ArtistModelFields.NAME_INTERNAL: name
        }
        model_fields.update(kwargs)
        return G(Artist, **model_fields)

    def create_album(self, name: str, user: User | None = None, **kwargs) -> Album:
        model_fields = {
            AlbumModelFields.CREATED_ON: timezone.make_aware(datetime.now()),
            AlbumModelFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            AlbumModelFields.USER: user or self.default_test_user,
            AlbumModelFields.ALBUM_ARTISTS: [],
            AlbumModelFields.YEAR: None,
            AlbumModelFields.NAME_INTERNAL: name
        }
        model_fields.update(kwargs)
        return G(Album, **model_fields)

    def create_genre(self, name: str, **kwargs) -> Genre:
        return self.__create_criteria(name=name, model_class=Genre, **kwargs)

    def create_tag(self, name: str, **kwargs) -> Tag:
        return self.__create_criteria(name=name, model_class=Tag, **kwargs)

    def create_manual_playlist(self, name: str, user: User | None = None, **kwargs) -> ManualPlaylist:
        now = timezone.make_aware(datetime.now())
        model_fields = {
            # Base Playlist fields
            PlayListFields.CREATED_ON: kwargs.get(PlayListFields.CREATED_ON, now),
            PlayListFields.UPDATED_ON: kwargs.get(PlayListFields.UPDATED_ON, now),
            PlayListFields.USER: user or self.default_test_user,
            PlayListFields.PLAY_COUNT: kwargs.get(PlayListFields.PLAY_COUNT, 0),
            # ManualPlaylist specific field
            ManualPlayListFields.NAME_PUBLIC: name,  # Maps to _name in the model
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

    def create_musicbrainz_artist(self, musicbrainz_id: str, name: str, **kwargs) -> MbArtist:
        model_fields = {
            MusicbrainzArtistFields.CREATED_ON: timezone.make_aware(datetime.now()),
            MusicbrainzArtistFields.UPDATED_ON: timezone.make_aware(datetime.now()),
            MusicbrainzArtistFields.MUSICBRAINZ_ID: musicbrainz_id,
            MusicbrainzArtistFields.NAME: name
        }
        model_fields.update(kwargs)
        return G(MbArtist, **model_fields)

    def create_spotify_lib_track(self, name: str, **kwargs) -> SpotifyLibTrack:
        model_fields = {
            TrackFields.SPOTIFY_ID: str(uuid.uuid4()),
            TrackFields.NAME: name,
            TrackFields.DURATION_MS: kwargs.get(TrackFields.DURATION_MS, 0),
            TrackFields.POPULARITY: kwargs.get(TrackFields.POPULARITY),
            TrackFields.ALBUM: kwargs.get(TrackFields.ALBUM),
            TrackFields.PREVIEW_URL: kwargs.get(TrackFields.PREVIEW_URL),
            TrackFields.EXPLICIT: kwargs.get(TrackFields.EXPLICIT, False),
            TrackFields.LAST_SYNCED_AT: kwargs.get(TrackFields.LAST_SYNCED_AT, timezone.make_aware(datetime.now())),
            TrackFields.IS_REMOVED: kwargs.get(TrackFields.IS_REMOVED, False)
        }
        track = G(SpotifyLibTrack, **model_fields)
        if 'spotify_artists' in kwargs:
            track.spotify_artists.set(kwargs['spotify_artists'])
        return track

    def create_spotify_artist(self, name: str, **kwargs) -> SpotifyArtist:
        model_fields = {
            ArtistFields.SPOTIFY_ID: str(uuid.uuid4()),
            ArtistFields.NAME: name,
            ArtistFields.POPULARITY: kwargs.get(ArtistFields.POPULARITY),
            ArtistFields.GENRES: kwargs.get(ArtistFields.GENRES, []),
            ArtistFields.IMAGES: kwargs.get(ArtistFields.IMAGES, []),
            ArtistFields.CREATED_ON: timezone.make_aware(datetime.now()),
            ArtistFields.UPDATED_ON: timezone.make_aware(datetime.now())
        }
        return G(SpotifyArtist, **model_fields)
