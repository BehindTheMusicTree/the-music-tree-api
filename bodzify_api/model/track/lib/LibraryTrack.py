from typing import TYPE_CHECKING, List, Tuple

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone

from bodzify_api import settings
from bodzify_api.model.field.AppCharField import AppCharField
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.model.criteria.Fields import Fields as CriteriaFields
from bodzify_api.model.field.foreign_key.PrivateForeignKey import PrivateForeignKey
from bodzify_api.model.field.foreign_key.PrivateManyToManyField import PrivateManyToManyField
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.model.album.Album import Album
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount
from bodzify_api.utils.audio_metadata.MetadataManager import METADATA_ARTISTS_SEPARATION_CHAR
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys
from ..file.TrackFile import TrackFile
from .Fields import Fields
from .LibTrackManager import LibTrackManager

if TYPE_CHECKING:
    from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel


class LibraryTrack(TrackablePlayCount):
    title = AppCharField(max_length=settings.LIB_TRACK_TITLE_LEN_MAX)
    track_file_fingerprint_must_be_unique = models.BooleanField(default=False)
    album: Album = PrivateForeignKey(Album,  # type: ignore
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     related_name=AlbumFields.LIB_TRACKS_RELATED_NAME,)
    position_in_album = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(settings.LIB_TRACK_POSITION_IN_ALBUM_MAX)])
    artists = PrivateManyToManyField(Artist, blank=True, related_name=ArtistFields.LIB_TRACKS_RELATED_NAME)
    genre = PrivateForeignKey(Genre,
                              on_delete=models.DO_NOTHING,
                              null=True,
                              blank=True,
                              related_name=CriteriaFields.LIB_TRACKS_RELATED_NAME)
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(settings.LIB_TRACK_RATING_VALUE_MAX)])
    language = AppCharField(max_length=settings.LIB_TRACK_LANGUAGE_LEN_MAX, blank=True, default=None, null=True)
    archived = models.BooleanField(default=False)
    playlists = PrivateManyToManyField(Playlist,
                                       through='LibTrackPlaylistRel',
                                       related_name=PlaylistFields.LIB_TRACKS_RELATED_NAME)

    if TYPE_CHECKING:
        track_file: TrackFile
        lib_track_playlist_rels: models.QuerySet['LibTrackPlaylistRel']

    objects: LibTrackManager = LibTrackManager()

    class Meta:
        verbose_name = 'Library Track'
        verbose_name_plural = 'Library Tracks'
        indexes = [models.Index(fields=[Fields.USER, Fields.TITLE]),
                   models.Index(fields=[Fields.USER, Fields.GENRE]),
                   models.Index(fields=[Fields.USER, Fields.ALBUM]),]

    @property
    def relative_url(self) -> str:
        return f"tracks/{self.uuid}/"

    def __str__(self):
        position_str = f"#{self.position_in_album}" if self.position_in_album else "#--"

        artists: QuerySet[Artist] = self.artists.all()
        artists_str = ", ".join(
            artist.name for artist in artists) if self.artists.exists() else f"[no {Fields.ARTISTS}]"
        album_str = str(self.album) if self.album else f"[no {Fields.ALBUM}]"

        genre_str = f"{Fields.GENRE}: {self.genre}" if self.genre else f"{Fields.GENRE}: --"
        rating_str = f"{Fields.RATING}: {self.rating}" if self.rating else f"{Fields.RATING}: --"
        language_str = f"{Fields.LANGUAGE}: {self.language}" if self.language else f"{Fields.LANGUAGE}: --"
        file_str = f"{Fields.TRACK_FILE}: {self.track_file}" if self.track_file else "no track file"

        return (f"{self.uuid} | {position_str} | {artists_str} - {self.title} | {album_str} | "
                f"{genre_str} | {rating_str} | {language_str} | "
                + f"{Fields.CREATED_ON}: {self.created_on} | {file_str}")

    def update_file_tags_from_lib_track_instance_values(self):
        normalized_metadata = dict()
        normalized_metadata[NormalizedMetadataKeys.TITLE] = self.title

        if self.artists.count() > 0:
            artists_names_tag = ""
            artists_list: list[Artist] = list(self.artists.all())
            for artist in artists_list:
                if artists_names_tag != "":
                    artists_names_tag = artists_names_tag + METADATA_ARTISTS_SEPARATION_CHAR
                artists_names_tag = artists_names_tag + artist.name
        else:
            artists_names_tag = ""
        normalized_metadata[NormalizedMetadataKeys.ARTISTS_NAMES_STR] = artists_names_tag

        album_artists_tag = ""
        if self.album:
            album_name_tag = self.album.name
            album_artists_name_index = 0
            album_artists_list = self.album.album_artists.all()
            for album_artist in album_artists_list:
                if album_artists_name_index != 0:
                    album_artists_tag = album_artists_tag + METADATA_ARTISTS_SEPARATION_CHAR
                album_artists_tag = album_artists_tag + album_artist.name
                album_artists_name_index = album_artists_name_index + 1
        else:
            album_name_tag = ""

        normalized_metadata[NormalizedMetadataKeys.ALBUM_NAME] = album_name_tag
        normalized_metadata[NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES_STR] = album_artists_tag
        normalized_metadata[NormalizedMetadataKeys.GENRE_NAME] = self.genre.name if self.genre else ""
        normalized_metadata[NormalizedMetadataKeys.RATING] = self.rating
        normalized_metadata[NormalizedMetadataKeys.LANGUAGE] = self.language if self.language else ""

        self.track_file.update_file_tags(normalized_metadata=normalized_metadata)

    @property
    def playlists_with_positions(self) -> List[Tuple[str, int]]:
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel, \
            Fields as LibTrackPlaylistRelFields
        lib_track_playlist_rels = LibTrackPlaylistRel.objects.filter(user=self.user, lib_track=self)
        return list(lib_track_playlist_rels.values_list(LibTrackPlaylistRelFields.PLAYLIST + '__uuid',
                                                        LibTrackPlaylistRelFields.POSITION))


@receiver(pre_delete, sender=settings.APP_NAME + '.LibraryTrack')
def handle_pre_delete(sender, instance: LibraryTrack, using, **kwargs):
    from bodzify_api.model.playlist.Playlist import Playlist
    now = timezone.now()
    playlists: List[Playlist] = list(instance.playlists.all())
    for playlist in playlists:
        playlist.last_track_list_update_date = now
        playlist.save()
