#!/usr/bin/env python

from django.db import models
from bodzify_api.model.LibTrackMixin \
    import LibTrackMixin, Fields as LibTrackMixinFields, SpecialNames as LibTrackMixinSpecialNames


class Fields:
    MODEL = 'all_lib_track_mixin'
    UUID = LibTrackMixinFields.UUID
    USER = LibTrackMixinFields.USER
    CREATED_ON = LibTrackMixinFields.CREATED_ON
    UPDATED_ON = LibTrackMixinFields.UPDATED_ON
    LIB_TRACKS = LibTrackMixinFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = LibTrackMixinFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = LibTrackMixinFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = LibTrackMixinFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackMixinFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = 'name'


class AllLibTrackMixin(LibTrackMixin):
    name = models.CharField(max_length=255, default=LibTrackMixinSpecialNames.ALL, editable=False)

    class Meta:
        db_table = f'bodzify_api_{Fields.MODEL}'
        verbose_name = 'All Library Track Mixin'
        verbose_name_plural = 'All Library Track Mixins'
        constraints = [models.UniqueConstraint(fields=[Fields.USER], name=f'unique_{Fields.USER}_{Fields.MODEL}')]

    def __str__(self):
        return f"{self.name} - {self.user}"

    @property
    def library_tracks(self):
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
        return LibraryTrack.objects.filter(user=self.user)

    @property
    def type_label(self):
        return "All Tracks"

    @classmethod
    def get_for_user(cls, user):
        return cls.objects.get(user=user)
