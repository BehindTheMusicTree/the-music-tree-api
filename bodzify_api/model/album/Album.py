from typing import List, Optional, TYPE_CHECKING
from django.db import models
from django.db.models import Q, QuerySet

from bodzify_api import settings
from bodzify_api.model.album.AlbumManager import AlbumManager
from bodzify_api.model.user.User import User
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.LibTrackMixin import LibTrackMixin

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack


class Album(LibTrackMixin):
    name = models.CharField(max_length=settings.ALBUM_NAME_LEN_MAX, default=None)
    year = models.CharField(max_length=4, default=None, null=True)
    album_artists = models.ManyToManyField(Artist, related_name=ArtistFields.ALBUMS)

    objects: AlbumManager = AlbumManager()

    @property
    def library_tracks(self) -> models.QuerySet['LibraryTrack']:
        return self.album_library_tracks  # type: ignore

    def get_sorted_tracks(self) -> models.QuerySet['LibraryTrack']:
        from bodzify_api.model.track.lib.Fields import Fields as LibraryTrackFields
        return self.library_tracks.annotate(
            null_position=Q(position_in_album__isnull=True)).order_by(
            'null_position', LibraryTrackFields.POSITION_IN_ALBUM, LibraryTrackFields.TITLE)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name="album_non_empty_name")]

    def __str__(self) -> str:
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

        string = f"{self.uuid} {self.name}"

        artists = list(self.album_artists.all())
        artist_names = " ".join(str(artist) for artist in artists) if artists else "[No Artist]"
        string += f" by {artist_names}"

        tracks: list[LibraryTrack] = list(self.library_tracks.all())
        if tracks:
            track_details = []
            for track in tracks:
                track_position = f"{track.position_in_album}." if track.position_in_album else "--."
                track_artists = ", ".join(str(artist) for artist in track.artists.all())
                track_artists = f"{track_artists} - " if track_artists else "[No Artist] - "
                track_details.append(f"{track_position}{track_artists}{track.title}")
            track_details_str = "; ".join(track_details)
            string += f" | Tracks: {track_details_str}"

        return string

    @staticmethod
    def create_with_album_artists_list(user: User, album_name: str, album_artists_list: list[Artist]) -> 'Album':
        album = Album.objects.create(user=user, name=album_name)
        if album_artists_list:
            album.album_artists.set(album_artists_list)
        return album

    @staticmethod
    def _get_album_from_name_and_artists_list_after_having_eventually_created_album(
            user: User, album_name: str, album_artists: list) -> Optional['Album']:

        album_queryset = Album.objects.filter(user=user, name=album_name)
        if len(album_artists) > 0:
            for album_artist in album_artists:
                album_queryset = album_queryset.filter(album_artists__in=[album_artist])
        else:
            album_queryset = album_queryset.filter(album_artists=None)

        if album_queryset.count() == 0:
            album = Album.create_with_album_artists_list(user=user,
                                                         album_name=album_name,
                                                         album_artists_list=album_artists)
        else:
            album = album_queryset.first()
        return album

    @staticmethod
    def get_album_from_name_and_album_artists_names_list_after_eventual_creations(
            user: User, album_name: str, album_artists_names_list: list) -> Optional['Album']:
        if album_artists_names_list and len(album_artists_names_list) > 0:
            album_artists = [Artist.objects.get_or_create(user=user, name=artist_name)[0]
                             for artist_name in album_artists_names_list]
        else:
            album_artists = []

        return Album._get_album_from_name_and_artists_list_after_having_eventually_created_album(
            user=user, album_name=album_name, album_artists=album_artists)

    def delete_with_tracks_and_eventually_artists(self):
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

        artists_linked_to_album_and_track: List[Artist] = []
        lib_tracks: QuerySet[LibraryTrack] = self.library_tracks.all()
        for track in lib_tracks:
            if track.artists.exists():
                for artist in track.artists.all():
                    if artist not in artists_linked_to_album_and_track:
                        artists_linked_to_album_and_track.append(artist)
            track.delete()

        for album_artist in self.album_artists.all():
            if album_artist not in artists_linked_to_album_and_track:
                artists_linked_to_album_and_track.append(album_artist)

        self.delete()

        for artist in artists_linked_to_album_and_track:
            artist.delete_if_nothing_linked()

    def delete_if_no_track_linked_with_eventual_album_artist_deletion(self):
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
        if self.library_tracks.count() == 0:
            album_artists: list[Artist] = list(self.album_artists.all())
            self.delete()
            for album_artist in album_artists:
                album_artist.delete_if_nothing_linked()
