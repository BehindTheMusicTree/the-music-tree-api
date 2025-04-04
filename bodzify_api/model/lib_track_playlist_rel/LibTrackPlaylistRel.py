from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Case, When, Value


from bodzify_api.model.field.foreign_key.PrivateForeignKey import PrivateForeignKey
from bodzify_api.model.uploaded_track_playlist_rel.LibTrackPlaylistRelManager import LibTrackPlaylistRelManager
from bodzify_api.model.playlist.Fields import Fields as PlayListFields
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from bodzify_api.model.track.lib.LibraryTrack import UploadedTrack

from .Fields import Fields


User = get_user_model()


class LibTrackPlaylistRel(PrivateStandardResource):
    playlist: Playlist = PrivateForeignKey(  # type: ignore
        Playlist, on_delete=models.CASCADE, related_name=PlayListFields.UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL)
    uploaded_track: UploadedTrack = PrivateForeignKey(  # type: ignore
        UploadedTrack, on_delete=models.CASCADE, related_name=LibTrackFields.UPLOADED_TRACK_PLAYLIST_RELS)
    position = models.PositiveIntegerField(null=True, blank=True)

    objects: LibTrackPlaylistRelManager = LibTrackPlaylistRelManager()

    class Meta:
        verbose_name = 'Library Track Playlist Relation'
        verbose_name_plural = 'Library Track Playlist Relations'
        indexes = [
            models.Index(fields=[Fields.USER, Fields.PLAYLIST]),
            models.Index(fields=[Fields.USER, Fields.UPLOADED_TRACK_INTERNAL]),
        ]

    def __str__(self):
        return (f'Playlist "{self.playlist.name}" | Lib track title "{self.uploaded_track.title}" | '
                f'Position {self.position} User {self.user}')

    def _perform_save(self, adding: bool, ctx) -> None:
        if adding:
            uploaded_track_playlist_rels = LibTrackPlaylistRel.objects.filter(user=self.user, playlist=self.playlist)
            uploaded_track_playlist_rels.update(
                position=Case(
                    When(**{Fields.POSITION + '__isnull': False}, then=F(Fields.POSITION) + 1),
                    default=Value(None)
                )
            )
            self.position = 1
        super()._perform_save(adding, ctx)
