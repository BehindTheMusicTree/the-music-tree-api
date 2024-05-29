import datetime
from pathlib import Path
from typing import List, Optional
import uuid
from ddf import G

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.TrackFile import TrackFile as TrackFile
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist
from bodzify_api.model.musicbrainz.MusicbrainzRecording import MusicbrainzRecording
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.TestUser import TestUser


# Primarily used to obtain correct type hinting, as opposed to unknown return types in DDF.
class ModelFixtureFactory:
    test_user: TestUser

    def __init__(self, test_user: TestUser) -> None:
        self.test_user = test_user

    def __create_criteria(self,
                          name: str,
                          type: int,
                          parent: Optional[Criteria] = None,
                          created_on: Optional[datetime.date] = datetime.date.today(),
                          updated_on: Optional[datetime.date] = datetime.date.today()) -> Criteria:
        return G(Criteria,
                 user=self.test_user.django_user,
                 name=name, type=type,
                 parent=parent,
                 created_on=created_on,
                 updated_on=updated_on)  # type: ignore

    def create_artist(self,
                      name: str,
                      created_on: Optional[datetime.date] = datetime.date.today(),
                      updated_on: Optional[datetime.date] = datetime.date.today()) -> Artist:
        return G(Artist, user=self.test_user.django_user, name=name, created_on=created_on, updated_on=updated_on)  # type: ignore

    def create_album(self,
                     name: str,
                     album_artists: List[Artist] = [],
                     year: Optional[int] = None,
                     created_on: Optional[datetime.date] = datetime.date.today(),
                     updated_on: Optional[datetime.date] = datetime.date.today()) -> Album:
        return G(Album,
                 user=self.test_user.django_user,
                 name=name,
                 album_artists=album_artists,
                 year=year,
                 created_on=created_on,
                 updated_on=updated_on)  # type: ignore

    def create_file(self, filename: str, created_on: Optional[datetime.date] = datetime.date.today()) -> TrackFile:
        return G(TrackFile,
                 user=self.test_user.django_user,
                 file=str(Path(self.test_user.lib_abs_path) / filename),
                 size_in_ko=None,
                 size_in_mo=None,
                 created_on=created_on)  # type: ignore

    def create_lib_track(self,
                         title: str,
                         track_file: Optional[TrackFile] = None,
                         artist: Optional[Artist] = None,
                         album: Optional[Album] = None,
                         genre: Optional[Criteria] = None,
                         rating: Optional[int] = None,
                         language: Optional[str] = None,
                         play_count: Optional[int] = 0,
                         created_on: Optional[datetime.date] = datetime.date.today(),
                         updated_on: Optional[datetime.date] = datetime.date.today()) -> LibraryTrack:
        if track_file is None:
            track_file = self.create_file(filename=self.test_user.lib_track_default_filename)
        return G(LibraryTrack,
                 user=self.test_user.django_user,
                 title=title,
                 track_file=track_file,
                 artist=artist,
                 album=album,
                 genre=genre,
                 rating=rating,
                 language=language,
                 play_count=play_count,
                 created_on=created_on,
                 updated_on=updated_on)  # type: ignore

    def create_musicbrainz_recording(
            self, uuid: uuid.UUID, title: str, duration_in_sec: int,
            musicbrainz_artists: Optional[list[MusicbrainzArtist]] = None, release_date: Optional[datetime.date] = None,
            created_on: Optional[datetime.date] = datetime.date.today(),
            updated_on: Optional[datetime.date] = datetime.date.today()) -> MusicbrainzRecording:
        return G(MusicbrainzRecording,
                 uuid=uuid,
                 title=title,
                 duration_in_sec=duration_in_sec,
                 release_date=release_date,
                 musicbrainz_artists=musicbrainz_artists,
                 created_on=created_on,
                 updated_on=updated_on)  # type: ignore

    def create_musicbrainz_artist(self,
                                  uuid: uuid.UUID,
                                  name: str,
                                  created_on: Optional[datetime.date] = datetime.date.today(),
                                  updated_on: Optional[datetime.date] = datetime.date.today()) -> MusicbrainzArtist:
        return G(MusicbrainzArtist, uuid=uuid, name=name, created_om=created_on, updated_on=updated_on)  # type: ignore

    def create_genre(self,
                     name: str,
                     parent: Optional[Criteria] = None,
                     created_on: Optional[datetime.date] = datetime.date.today(),
                     updated_on: Optional[datetime.date] = datetime.date.today()) -> Criteria:
        return self.__create_criteria(
            name=name, type=CRITERIA_TYPES_ID.GENRE, parent=parent, created_on=created_on, updated_on=updated_on)

    def create_tag(self,
                   name: str,
                   parent: Optional[Criteria] = None,
                   created_on: Optional[datetime.date] = datetime.date.today(),
                   updated_on: Optional[datetime.date] = datetime.date.today()) -> Criteria:
        return self.__create_criteria(
            name=name, type=CRITERIA_TYPES_ID.TAG, parent=parent, created_on=created_on, updated_on=updated_on)

    def create_simple_playlist(self,
                               name,
                               play_count: Optional[int] = 0,
                               created_on: Optional[datetime.date] = datetime.date.today(),
                               updated_on: Optional[datetime.date] = datetime.date.today()) -> SimplePlaylist:
        return G(SimplePlaylist,
                 base_playlist__user=self.test_user.django_user,
                 name=name,
                 base_playlist__play_count=play_count,
                 base_playlist__created_on=created_on,
                 updated_on=updated_on)  # type: ignore
