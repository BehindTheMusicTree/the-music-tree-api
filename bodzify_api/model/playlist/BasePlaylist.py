from typing import Optional
from django.db import models
from django.utils import timezone

from bodzify_api import settings
from bodzify_api.model.base.TrackablePlayCountModel import TrackablePlayCountModel, Fields as TrackablePlayCountFields
from bodzify_api.model.LibTrackMixin import LibTrackMixin, Fields as LibTrackMixinFields


class Fields:
    MODEL = 'base_playlist'
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
    PLAY_COUNT = TrackablePlayCountFields.PLAY_COUNT
    NAME = 'name'
    CRITERIA_CHILD_PLAYLIST = 'criteria_child_playlist'
    SIMPLE_CHILD_PLAYLIST = 'simple_child_playlist'
    PLAYLIST_LIB_TRACK_RELATIONS = 'lib_track_position_relations'
    LAST_TRACK_LIST_UPDATE_DATE = 'last_track_list_update_date'


class BasePlaylist(LibTrackMixin, TrackablePlayCountModel):
    last_track_list_update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = f'{settings.APP_NAME}_base_playlist'
        verbose_name = 'Base Playlist'
        verbose_name_plural = 'Base Playlists'
        indexes = [models.Index(fields=[Fields.USER, Fields.UUID], name='base_playlist_user_uuid_idx')]

    @property
    def library_tracks(self) -> models.QuerySet['LibraryTrack']:  # type: ignore
        return self.playlist_library_tracks  # type: ignore

    @property
    def criteria_child_playlist(self) -> Optional['CriteriaPlaylist']:  # type: ignore
        return self.criteria_child_playlist

    @property
    def simple_child_playlist(self) -> Optional['ManualPlaylist']:  # type: ignore
        return self.simple_child_playlist

    @property
    def name(self) -> Optional[str]:
        if hasattr(self, Fields.CRITERIA_CHILD_PLAYLIST):
            return self.criteria_child_playlist.name  # type: ignore
        elif hasattr(self, Fields.SIMPLE_CHILD_PLAYLIST):
            return self.simple_child_playlist.name  # type: ignore
        else:
            return None

    @property
    def type_label(self) -> Optional[str]:
        if hasattr(self, Fields.CRITERIA_CHILD_PLAYLIST):
            return self.criteria_child_playlist.type.label  # type: ignore
        elif hasattr(self, Fields.SIMPLE_CHILD_PLAYLIST):
            return self.simple_child_playlist.type  # type: ignore
        else:
            return None

    def update_last_track_list_update_date(self):
        self.last_track_list_update_date = timezone.now()
        self.save()
        return self.last_track_list_update_date
