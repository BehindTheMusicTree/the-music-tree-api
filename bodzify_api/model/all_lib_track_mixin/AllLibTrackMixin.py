from django.db import models

from bodzify_api import settings
from ..lib_track_mixin.LibTrackMixin import LibTrackMixin
from .Fields import Fields


class AllLibTrackMixin(LibTrackMixin):
    class Meta:
        db_table = f'{settings.APP_NAME}_{Fields.MODEL}'
        verbose_name = 'All Library Track Mixin'
        verbose_name_plural = 'All Library Track Mixins'
        constraints = [models.UniqueConstraint(fields=[Fields.USER], name=f'unique_{Fields.USER}_{Fields.MODEL}')]

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
    def type(self):
        return "All Tracks"

    @classmethod
    def get_for_user(cls, user):
        return cls.objects.get(user=user)
