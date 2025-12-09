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

from api.model.album.Album import Album
from api.model.artist.Artist import Artist
from api.model.artist.Fields import Fields as ArtistFields
from api.model.criteria.children.genre.Genre import Genre
from api.model.criteria.children.tag.Tag import Tag
from api.model.criteria.Criteria import Criteria
from api.model.criteria.Criteria import Fields as CriteriaFields
from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
from api.model.track_playlist_rel.Fields import Fields as TrackPlaylistRelFields
from api.model.musicbrainz_resource.children.artist.Fields import Fields as MusicbrainzArtistFields
from api.model.musicbrainz_resource.children.artist.MbArtist import MbArtist
from api.model.musicbrainz_resource.children.recording.MbRecording import Fields as MusicbrainzRecordingFields
from api.model.musicbrainz_resource.children.recording.MbRecording import MusicbrainzRecording
from api.model.play.Fields import Fields as PlayFields
from api.model.play.Play import Play
from api.model.playlist.Playlist import Playlist
from api.model.playlist.children.manual.Fields import Fields as ManualPlayListFields
from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.model.playlist.Fields import Fields as PlayListFields
from api.model.track.Fields import Fields as TrackFields
from api.model.track.Track import Track
from api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount
from api.model.user.User import User
from api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from api.model.spotify_resource.children.track.Fields import Fields as TrackFields
from api.model.spotify_resource.children.artist.Fields import Fields as ArtistFields
from api.model.artist.Fields import Fields as ArtistModelFields
from api.model.album.Fields import Fields as AlbumModelFields


global_settings.DDF_FIELD_FIXTURES['django.db.models.fields.generated.GeneratedField'] = lambda: None  # type: ignore


class ModelFixtureFactory:
    default_test_user: 'User'

    def __init__(self, default_test_user: 'User') -> None:
        self.default_test_user = default_test_user

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

    def _create_track(self, user: User, title: str | None = None, **kwargs) -> Track:
        now = timezone.make_aware(datetime.now())
        model_fields = {
            TrackFields.CREATED_ON: kwargs.get(TrackFields.CREATED_ON, now),
            TrackFields.UPDATED_ON: kwargs.get(TrackFields.UPDATED_ON, now),
            TrackFields.USER: user,
            TrackFields.TITLE: title or "Untitled",
        }
        model_fields.update(kwargs)
        track = G(Track, **model_fields)

        if kwargs.get(TrackFields.ARTISTS):
            track.artists.set(kwargs[TrackFields.ARTISTS])

        return track

    def create_track_playlist_rel(
            self, playlist: Playlist, track: Track, user: User | None = None,) -> TrackPlaylistRel:
        model_fields = {
            TrackPlaylistRelFields.USER: user or self.default_test_user,
            TrackPlaylistRelFields.PLAYLIST: playlist,
            TrackPlaylistRelFields.UPLOADED_TRACK_INTERNAL: track,
        }
        return G(TrackPlaylistRel, **model_fields)

    def create_track_with_file(
        self,
        title: str | None = "test",
        user: User | None = None,
        **kwargs
    ) -> Track:
        return self._create_track(user=user or self.default_test_user, title=title, **kwargs)

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
