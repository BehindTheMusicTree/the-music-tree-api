from pathlib import Path
from typing import List, Optional
from django.contrib.auth.models import User
from ddf import G
from django.core.files import File as DjangoFile

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.File import File as AppFile
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack


# Primarily used to obtain correct type hinting, as opposed to unknown return types in DDF.
class ModelFixtureFactory:
    test_user: User
    lib_track_default_file: DjangoFile

    def __init__(self, test_user: User, lib_track_default_file_path) -> None:
        self.test_user = test_user
        self.lib_track_default_file = DjangoFile(lib_track_default_file_path)

    def create_artist(self, name: str) -> Artist:
        return G(Artist, user=self.test_user, name=name)  # type: ignore

    def create_album(self, name: str, album_artists: List[Artist] = [], year: Optional[int] = None) -> Album:
        return G(Album, user=self.test_user, name=name, album_artists=album_artists, year=year)  # type: ignore

    def create_file(self, file_path: Path) -> AppFile:
        return G(AppFile, user=self.test_user, file=file_path, size_in_ko=None, size_in_mo=None)  # type: ignore

    def create_lib_track(self,
                         title: str,
                         file_obj: Optional[AppFile] = None,
                         artist: Optional[Artist] = None,
                         album: Optional[Album] = None,
                         genre: Optional[Criteria] = None,
                         rating: Optional[int] = None,
                         language: Optional[str] = None,
                         play_count: Optional[int] = 0) -> LibraryTrack:
        if file_obj is None:
            file_obj = self.create_file(file_path=self.lib_track_default_file)
        return G(LibraryTrack,
                 user=self.test_user,
                 title=title,
                 file_obj=file_obj,
                 artist=artist,
                 album=album,
                 genre=genre,
                 rating=rating,
                 language=language,
                 play_count=play_count)  # type: ignore

    def create_criteria(self, name: str, type: int, parent: Optional[Criteria] = None) -> Criteria:
        return G(Criteria, user=self.test_user, name=name, type=type, parent=parent)  # type: ignore

    def create_genre(self, name: str, parent: Optional[Criteria] = None) -> Criteria:
        return self.create_criteria(name=name, type=CRITERIA_TYPES_ID.GENRE, parent=parent)

    def create_tag(self, name: str, parent: Optional[Criteria] = None) -> Criteria:
        return self.create_criteria(name=name, type=CRITERIA_TYPES_ID.TAG, parent=parent)

    def create_simple_playlist(self, name, play_count: Optional[int] = 0) -> SimplePlaylist:
        return G(SimplePlaylist, playlist__user=self.test_user, name=name, playlist__play_count=play_count)  # type: ignore
