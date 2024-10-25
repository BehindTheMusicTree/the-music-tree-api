#!/usr/bin/env python

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models import QuerySet

from bodzify_api.model.track.lib.LibraryTrackManager import LibraryTrackManager
from bodzify_api import settings
from bodzify_api.model.base.PrivateUniqueResource import PrivateUniqueResource
from bodzify_api.model.track.lib.Fields import Fields
from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.TrackablePlayCountModel import TrackablePlayCountModel
from bodzify_api.model.criteria.Criteria import Criteria


class LibraryTrack(PrivateUniqueResource, TrackablePlayCountModel):
    title = models.CharField(max_length=settings.LIB_TRACK_TITLE_LEN_MAX)
    track_file_fingerprint_must_be_unique = models.BooleanField(default=False)

    album = models.ForeignKey(Album,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,
                              related_name=f"album_{Fields.MODEL}s",)
    position_in_album = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(settings.LIB_TRACK_POSITION_IN_ALBUM_MAX)]
    )
    artists = models.ManyToManyField(Artist, blank=True, related_name=f'{Fields.MODEL}s')
    genre = models.ForeignKey(Criteria,
                              on_delete=models.DO_NOTHING,
                              null=True,
                              blank=True,
                              related_name=f"{Fields.MODEL}s")
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(settings.LIB_TRACK_RATING_VALUE_MAX)])
    language = models.CharField(max_length=settings.LIB_TRACK_LANGUAGE_LEN_MAX, blank=True, default=None, null=True)
    archived = models.BooleanField(default=False)
    base_playlists = models.ManyToManyField('BasePlaylist',
                                            through='LibTrackPlaylistPositionRel',
                                            related_name=f"playlist_{Fields.MODEL}s")

    objects: LibraryTrackManager = LibraryTrackManager()

    class Meta:
        db_table = 'bodzify_api_library_track'
        verbose_name = 'Library Track'
        verbose_name_plural = 'Library Tracks'
        indexes = [
            models.Index(fields=[Fields.USER, Fields.TITLE]),
            models.Index(fields=[Fields.USER, Fields.GENRE]),
            models.Index(fields=[Fields.USER, Fields.ALBUM]),
        ]

    @property
    def track_file(self) -> TrackFile:
        return self._track_file  # type: ignore

    @property
    def lib_track_playlist_relations(self) -> models.QuerySet:
        return self.lib_track_position_relations  # type: ignore

    @property
    def relative_url(self) -> str:
        return f"tracks/{self.uuid}/"

    def __str__(self):
        position_str = f"#{self.position_in_album}" if self.position_in_album else "#--"

        artists: QuerySet[Artist] = self.artists.all()
        artists_str = ", ".join(artist.name for artist in artists) if self.artists.exists() else "[No Artist]"
        album_str = str(self.album) if self.album else "[No Album]"

        genre_str = f"{Fields.GENRE}: {self.genre}" if self.genre else f"{Fields.GENRE}: --"
        rating_str = f"{Fields.RATING}: {self.rating}" if self.rating else f"{Fields.RATING}: --"
        language_str = f"{Fields.LANGUAGE}: {self.language}" if self.language else f"{Fields.LANGUAGE}: --"
        file_str = f"{Fields.TRACK_FILE_DB}: {self.track_file}" if self.track_file else "No track file"

        return (f"{self.uuid} | {position_str} | {artists_str} - {self.title} | {album_str} | "
                f"{genre_str} | {rating_str} | {language_str} | "
                + f"{Fields.CREATED_ON}: {self.created_on} | {file_str}")

    def delete_with_checking_album_and_artists_potential_deletion(self):
        artists: QuerySet[Artist] = self.artists.all()
        self.delete()
        if self.album:
            self.album.delete_if_no_track_linked_with_eventual_album_artist_deletion()
        if artists.count() > 0:
            for artist in artists:
                artist.delete_if_nothing_linked()

    def delete_with_checking_artists_potential_deletion(self):
        track_artists: QuerySet[Artist] = self.artists.all()
        self.delete()
        for artist in track_artists:
            artist.delete_if_nothing_linked()

    def delete_with_checking_album_potential_deletion(self):
        track_album = self.album
        self.delete()
        if track_album:
            track_album.delete_if_no_track_linked_with_eventual_album_artist_deletion()


@receiver(pre_delete, sender=LibraryTrack)
def handle_pre_delete(sender, instance: 'LibraryTrack', using, **kwargs):
    instance.objects.handle_pre_delete(instance)
