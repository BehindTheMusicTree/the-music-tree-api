from django.db import models

from api.model.all_uploaded_tracks_mixin.AllUploadedTrackMixinManager import AllUploadedTrackMixinManager
from api.model.uploaded_track.UploadedTrack import UploadedTrack

from ..uploaded_track_mixin.UploadedTrackMixin import UploadedTrackMixin
from .Fields import Fields


# One per user
class AllUploadedTracksMixin(UploadedTrackMixin):

    objects: AllUploadedTrackMixinManager = AllUploadedTrackMixinManager()

    class Meta:
        verbose_name = 'All Uploaded Tracks Mixin'
        verbose_name_plural = 'All Uploaded Tracks Mixins'
        constraints = [models.UniqueConstraint(fields=[Fields.USER], name=f'unique_{Fields.USER}_all_tracks_mixin')]

    def __str__(self):
        return f"{self.name} | {self.user}"

    @property
    def name(self):
        return 'All Tracks'

    @property
    def uploaded_tracks(self) -> models.QuerySet[UploadedTrack]:
        return UploadedTrack.objects.filter(user=self.user)

    @property
    def type(self):
        return "All Uploaded Tracks"
