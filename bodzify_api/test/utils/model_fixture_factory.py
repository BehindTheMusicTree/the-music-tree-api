
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, cast

from ddf import G, N
from django_dynamic_fixture import global_settings
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import get_user_model

from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaType, CriteriaTypesId
from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist
from bodzify_api.model.musicbrainz.recording.MusicbrainzRecording import MusicbrainzRecording
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.children.ManualPlaylist import ManualPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.file.TrackFile import TrackFile as TrackFile
from bodzify_api.model.user.User import User

# Configure DDF to handle generated fields
global_settings.DDF_FIELD_FIXTURES['django.db.models.fields.generated.GeneratedField'] = lambda: None


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
        """Create a test user without recursive dependencies"""
        UserModel = get_user_model()
        unique_id = str(uuid.uuid4())[:8]
        # Use N() to create without recursion, then save manually
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
                          type: int,
                          parent: Optional[Criteria] = None,
                          created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                          updated_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                          user: Optional['User'] = None) -> Criteria:
        # Create criteria instance directly to avoid recursion
        criteria = Criteria.objects.create(
            created_on=created_on,
            updated_on=updated_on,
            user=user or self.default_test_user,
            name=name,
            parent=parent,
            type_id=type
        )

        return criteria

    def _create_file(self,
                     lib_track: LibraryTrack,
                     filename: Optional[str],
                     created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                     updated_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                     user: Optional['User'] = None) -> TrackFile:

        user = user or self.default_test_user

        if not os.path.exists(user.lib_abs_path):
            os.makedirs(user.lib_abs_path)

        file_path = self.lib_samples_dir / filename if filename else self.generic_sample_path

        track_file_path_in_lib = user.lib_abs_path / os.path.basename(file_path)
        shutil.copy(file_path, track_file_path_in_lib)

        return G(TrackFile,
                 created_on=created_on,
                 updated_on=updated_on,
                 user=user,
                 library_track=lib_track,
                 file=str(track_file_path_in_lib),
                 size_in_ko=None,
                 size_in_mo=None,)

    def _create_lib_track(self,
                          title: str,
                          artists: Optional[list[Artist]] = [],
                          album: Optional[Album] = None,
                          position_in_album: Optional[int] = None,
                          genre: Optional[Criteria] = None,
                          rating: Optional[int] = None,
                          language: Optional[str] = None,
                          play_count: Optional[int] = 0,
                          archived: Optional[bool] = False,
                          created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                          updated_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                          user: Optional['User'] = None) -> LibraryTrack:
        library_track = G(LibraryTrack,
                          user=user or self.default_test_user,
                          created_on=created_on,
                          updated_on=updated_on,
                          title=title,
                          album=album,
                          position_in_album=position_in_album,
                          genre=genre,
                          rating=rating,
                          language=language,
                          play_count=play_count,
                          archived=archived,)
        if artists:
            library_track.artists.set(artists)
        return library_track

    def create_artist(self,
                      name: str,
                      created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                      updated_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                      user: Optional['User'] = None) -> Artist:
        return G(Artist,
                 created_on=created_on,
                 updated_on=updated_on,
                 user=user or self.default_test_user,
                 name=name,)

    def create_album(self,
                     name: str,
                     album_artists: List[Artist] = [],
                     year: Optional[int] = None,
                     created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                     updated_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                     user: Optional['User'] = None) -> Album:
        return G(Album,
                 created_on=created_on,
                 updated_on=updated_on,
                 user=user or self.default_test_user,
                 name=name,
                 album_artists=album_artists,
                 year=year,)

    def create_lib_track_with_file(self,
                                   title: str,
                                   filename: Optional[str] = None,
                                   artists: Optional[list[Artist]] = None,
                                   album: Optional[Album] = None,
                                   position_in_album: Optional[int] = None,
                                   genre: Optional[Criteria] = None,
                                   rating: Optional[int] = None,
                                   language: Optional[str] = None,
                                   play_count: Optional[int] = 0,
                                   archived: Optional[bool] = False,
                                   created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                                   updated_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                                   user: Optional['User'] = None) -> LibraryTrack:

        with transaction.atomic():
            library_track = self._create_lib_track(title=title,
                                                   artists=artists,
                                                   album=album,
                                                   position_in_album=position_in_album,
                                                   genre=genre,
                                                   rating=rating,
                                                   language=language,
                                                   play_count=play_count,
                                                   archived=archived,
                                                   created_on=created_on,
                                                   updated_on=updated_on,
                                                   user=user)

            self._create_file(lib_track=library_track,
                              filename=filename,
                              created_on=created_on,
                              user=user)

        return library_track

    def create_musicbrainz_recording(
            self, uuid: uuid.UUID,
            title: str,
            duration_in_sec: int,
            musicbrainz_artists: Optional[list[MusicbrainzArtist]] = None,
            release_date: Optional[datetime] = None,
            created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
            updated_on: Optional[datetime] = timezone.make_aware(datetime.now())) -> MusicbrainzRecording:
        return G(MusicbrainzRecording,
                 uuid=uuid,
                 created_on=created_on,
                 updated_on=updated_on,
                 title=title,
                 duration_in_sec=duration_in_sec,
                 release_date=release_date,
                 musicbrainz_artists=musicbrainz_artists,)

    def create_musicbrainz_artist(
            self,
            musicbrainz_id: str,
            name: str,
            created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
            updated_on: Optional[datetime] = timezone.make_aware(datetime.now())) -> MusicbrainzArtist:
        return G(MusicbrainzArtist,
                 musicbrainz_id=musicbrainz_id,
                 name=name,
                 created_om=created_on,
                 updated_on=updated_on)

    def create_genre(self,
                     name: str,
                     parent: Optional[Criteria] = None,
                     created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                     updated_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                     user: Optional['User'] = None) -> Criteria:
        return self.__create_criteria(created_on=created_on,
                                      updated_on=updated_on,
                                      user=user,
                                      name=name,
                                      type=CriteriaTypesId.GENRE,
                                      parent=parent,)

    def create_tag(self,
                   name: str,
                   parent: Optional[Criteria] = None,
                   created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                   updated_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                   user: Optional['User'] = None) -> Criteria:
        return self.__create_criteria(created_on=created_on,
                                      updated_on=updated_on,
                                      user=user,
                                      name=name,
                                      type=CriteriaTypesId.TAG,
                                      parent=parent,)

    def create_manual_playlist(self,
                               name,
                               play_count: Optional[int] = 0,
                               created_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                               updated_on: Optional[datetime] = timezone.make_aware(datetime.now()),
                               user: Optional['User'] = None) -> ManualPlaylist:
        base_playlist = G(BasePlaylist,
                          created_on=created_on,
                          updated_on=updated_on,
                          user=user or self.default_test_user,
                          play_count=play_count)
        return G(ManualPlaylist,
                 base_playlist=base_playlist,
                 name=name,)
