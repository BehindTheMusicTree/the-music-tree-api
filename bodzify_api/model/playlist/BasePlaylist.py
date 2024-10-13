#!/usr/bin/env python

from typing import Optional
from django.db import models
from django.template import Library
from django.utils import timezone

from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin, \
    AttributesLabels as LibTrackMixinAttributesLabels


class SpecialNames:
    ALL = 'All'
    GENRELESS = 'Genreless'


class AttributesLabels:
    MODEL = 'base_playlist'
    UUID = LibTrackMixinAttributesLabels.UUID
    USER = LibTrackMixinAttributesLabels.USER
    CREATED_ON = LibTrackMixinAttributesLabels.CREATED_ON
    UPDATED_ON = LibTrackMixinAttributesLabels.UPDATED_ON
    LIB_TRACKS = LibTrackMixinAttributesLabels.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = LibTrackMixinAttributesLabels.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = LibTrackMixinAttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = LibTrackMixinAttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = LibTrackMixinAttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackMixinAttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = 'name'
    TYPE_LABEL = 'type_label'
    CRITERIA_PLAYLIST_CHILD = 'criteria_playlist_child'
    SIMPLE_PLAYLIST_CHILD = 'simple_playlist_child'
    PLAY_COUNT = 'play_count'
    PLAYLIST_LIB_TRACK_RELATIONS = 'lib_track_position_relations'
    LAST_TRACK_LIST_UPDATE_DATE = 'last_track_list_update_date'


FOREIGN_MODEL_ATTRIBUTES_PREFIXE = 'base_playlist_'


class ForeignModelAttributesLabel:
    UUID = ''
    USER = ''
    CREATED_ON = ''
    UPDATED_ON = ''
    NAME = ''
    TYPE = ''
    LIB_TRACKS = ''
    LIB_TRACKS_NOT_ARCHIVED = ''
    LIB_TRACKS_COUNT = ''
    LIB_TRACKS_ARCHIVED_COUNT = ''
    PLAY_COUNT = ''
    PLAYLIST_LIB_TRACK_RELATIONS = ''


for attr, value in vars(AttributesLabels).items():
    if not attr.startswith("__"):
        setattr(ForeignModelAttributesLabel, attr, FOREIGN_MODEL_ATTRIBUTES_PREFIXE + value)

FOREIGN_MODEL_RELATIONS_PREFIXE = 'base_playlist.'


class ForeignModelRelationsStr:
    UUID = ''
    USER = ''
    CREATED_ON = ''
    UPDATED_ON = ''
    NAME = ''
    TYPE = ''
    LIB_TRACKS = ''
    LIB_TRACKS_NOT_ARCHIVED = ''
    LIB_TRACKS_COUNT = ''
    LIB_TRACKS_ARCHIVED_COUNT = ''
    PLAY_COUNT = ''
    PLAYLIST_LIB_TRACK_RELATIONS = ''


for attr, value in vars(AttributesLabels).items():
    if not attr.startswith("__"):
        setattr(ForeignModelRelationsStr, attr, FOREIGN_MODEL_RELATIONS_PREFIXE + value)


class BasePlaylist(LibTrackMixin):
    play_count = models.IntegerField(default=0)
    last_track_list_update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bodzify_api_base_playlist'
        verbose_name = 'Base Playlist'
        verbose_name_plural = 'Base Playlists'

    @property
    def library_tracks(self) -> models.QuerySet['LibraryTrack']:  # type: ignore
        return self.playlist_library_tracks  # type: ignore

    @property
    def criteria_playlist_child(self) -> Optional['CriteriaPlaylist']:  # type: ignore
        return self.criteria_playlist_child

    @property
    def simple_playlist_child(self) -> Optional['SimplePlaylist']:  # type: ignore
        return self.simple_playlist_child

    @property
    def name(self) -> Optional[str]:
        if hasattr(self, AttributesLabels.CRITERIA_PLAYLIST_CHILD):
            return self.criteria_playlist_child.name  # type: ignore
        elif hasattr(self, AttributesLabels.SIMPLE_PLAYLIST_CHILD):
            return self.simple_playlist_child.name  # type: ignore
        else:
            return None

    @property
    def type_label(self) -> Optional[str]:
        if hasattr(self, AttributesLabels.CRITERIA_PLAYLIST_CHILD):
            return self.criteria_playlist_child.type.label  # type: ignore
        elif hasattr(self, AttributesLabels.SIMPLE_PLAYLIST_CHILD):
            return self.simple_playlist_child.type  # type: ignore
        else:
            return None

    def update_last_track_list_update_date(self):
        self.last_track_list_update_date = timezone.now()
        self.save()
        return self.last_track_list_update_date
