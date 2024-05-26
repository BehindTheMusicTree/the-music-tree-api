from pathlib import Path
from typing import List, Optional
from ddf import G

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.TrackFile import TrackFile as TrackFile
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.TestUser import TestUser


# Primarily used to obtain correct type hinting, as opposed to unknown return types in DDF.
class ModelFixtureFactory:
    test_user: TestUser

    def __init__(self, test_user: TestUser) -> None:
        self.test_user = test_user

    def __create_criteria(self, name: str, type: int, parent: Optional[Criteria] = None) -> Criteria:
        return G(Criteria, user=self.test_user.django_user, name=name, type=type, parent=parent)  # type: ignore

    def create_artist(self, name: str) -> Artist:
        return G(Artist, user=self.test_user.django_user, name=name)  # type: ignore

    def create_album(self, name: str, album_artists: List[Artist] = [], year: Optional[int] = None) -> Album:
        return G(Album, user=self.test_user.django_user, name=name, album_artists=album_artists, year=year)  # type: ignore

    def create_file(self, filename: str) -> TrackFile:
        return G(TrackFile,
                 user=self.test_user.django_user,
                 file=str(Path(self.test_user.lib_abs_path) / filename),
                 size_in_ko=None, size_in_mo=None)  # type: ignore

    def create_lib_track(self,
                         title: str,
                         track_file: Optional[TrackFile] = None,
                         artist: Optional[Artist] = None,
                         album: Optional[Album] = None,
                         genre: Optional[Criteria] = None,
                         rating: Optional[int] = None,
                         language: Optional[str] = None,
                         play_count: Optional[int] = 0) -> LibraryTrack:
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
                 play_count=play_count)  # type: ignore

    def create_genre(self, name: str, parent: Optional[Criteria] = None) -> Criteria:
        return self.__create_criteria(name=name, type=CRITERIA_TYPES_ID.GENRE, parent=parent)

    def create_tag(self, name: str, parent: Optional[Criteria] = None) -> Criteria:
        return self.__create_criteria(name=name, type=CRITERIA_TYPES_ID.TAG, parent=parent)

    def create_simple_playlist(self, name, play_count: Optional[int] = 0) -> SimplePlaylist:
        return G(SimplePlaylist, playlist__user=self.test_user.django_user, name=name, playlist__play_count=play_count)  # type: ignore
