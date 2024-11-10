from django.db import models

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.lib.Fields import Fields as LibraryTrackFields

from ..lib_track_mixin.LibTrackMixin import LibTrackMixin
from .Fields import Fields


class AllLibTracksMixin(LibTrackMixin):
    class Meta:
        verbose_name = 'All Library Tracks Mixin'
        verbose_name_plural = 'All Library Tracks Mixins'
        constraints = [models.UniqueConstraint(fields=[Fields.USER], name=f'unique_{Fields.USER}_all_tracks_mixin')]

    def __str__(self):
        return f"{self.name} | {self.user}"

    @property
    def name(self):
        return 'All Tracks'

    @property
    def library_tracks(self):
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
        return LibraryTrack.objects.filter(user=self.user)

    @property
    def lib_tracks_sorted(self) -> models.QuerySet['LibraryTrack']:
        return self.library_tracks.order_by(f'-{LibraryTrackFields.CREATED_ON}')

    @property
    def type(self):
        return "All Tracks"
