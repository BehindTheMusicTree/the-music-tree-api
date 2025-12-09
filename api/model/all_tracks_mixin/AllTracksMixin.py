from django.db import models

from api.model.all_tracks_mixin.AllTrackMixinManager import AllTrackMixinManager
from api.model.track.Track import Track

from ..track_mixin.TrackMixin import TrackMixin
from .Fields import Fields


# One per user
class AllTracksMixin(TrackMixin):

    objects: AllTrackMixinManager = AllTrackMixinManager()

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
    def tracks(self) -> models.QuerySet[Track]:
        return Track.objects.filter(user=self.user)

    @property
    def type(self):
        return "All Uploaded Tracks"
