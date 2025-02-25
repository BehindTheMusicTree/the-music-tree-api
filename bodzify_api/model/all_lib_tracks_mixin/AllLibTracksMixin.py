from django.db import models

from bodzify_api.model.all_lib_tracks_mixin.AllLibTrackMixinManager import \
    AllLibTrackMixinManager
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

from ..lib_track_mixin.LibTrackMixin import LibTrackMixin
from .Fields import Fields


# One per user
class AllLibTracksMixin(LibTrackMixin):

    objects: AllLibTrackMixinManager = AllLibTrackMixinManager()

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
    def lib_tracks(self) -> models.QuerySet[LibraryTrack]:
        return LibraryTrack.objects.filter(user=self.user)

    @property
    def type(self):
        return "All Tracks"
