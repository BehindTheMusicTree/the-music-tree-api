#!/usr/bin/env python

from django.db import models

from bodzify_api.model.criteria.Criteria import Criteria, Fields as ModelFields
from bodzify_api.model.criteria.CriteriaType import CriteriaType, CriteriaTypesId
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist, Fields as BasePlaylistFields
from bodzify_api.model.playlist.children.ChildPlaylist import ChildPlaylist, Fields as ChildFields
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylistManager import CriteriaPlaylistManager


class SpecialNames:
    GENRELESS = 'Genreless'
    TAGLESS = 'Tagless'


class TypesLabel:
    GENRE = 'genre'
    TAG = 'tag'


class Fields:
    BASE_PLAYLIST = ChildFields.BASE_PLAYLIST
    UUID = ChildFields.UUID
    USER = ChildFields.USER
    CREATED_ON = ChildFields.CREATED_ON
    UPDATED_ON = ChildFields.UPDATED_ON
    LIB_TRACKS = ChildFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = ChildFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = ChildFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ChildFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ChildFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildFields.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = ChildFields.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = ChildFields.LAST_TRACK_LIST_UPDATE_DATE
    CRITERIA = 'criteria'
    TYPE = 'type'
    PARENT = 'parent'
    ROOT = 'root'
    NAME = 'name'


class CriteriaPlaylist(ChildPlaylist):
    base_playlist = models.OneToOneField(BasePlaylist,
                                         on_delete=models.CASCADE,
                                         primary_key=True,
                                         related_name=BasePlaylistFields.CRITERIA_CHILD_PLAYLIST)
    criteria = models.OneToOneField(Criteria,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    related_name=ModelFields.CRITERIA_PLAYLIST)
    type = models.ForeignKey(CriteriaType,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=False)

    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               related_name='child_playlist')
    root = models.ForeignKey('self',
                             on_delete=models.CASCADE,
                             related_name='descendant_playlist')

    objects: CriteriaPlaylistManager = CriteriaPlaylistManager()

    class Meta:
        db_table = 'bodzify_api_criteria_playlist'
        verbose_name = 'Criteria Playlist'
        verbose_name_plural = 'Criteria Playlists'
        indexes = [
            models.Index(fields=[Fields.BASE_PLAYLIST, Fields.CRITERIA],
                         name='criteria_playlist_idx'),
        ]

    @property
    def name(self):
        if self.criteria is None:
            if self.type.pk == CriteriaTypesId.GENRE:
                return SpecialNames.GENRELESS
            elif self.type.pk == CriteriaTypesId.TAG:
                return SpecialNames.TAGLESS
        else:
            return self.criteria.name

    @property
    def children(self) -> models.QuerySet['CriteriaPlaylist']:
        return CriteriaPlaylist.objects.get_children(self.user, self)

    def __str__(self) -> str:
        return f'{self.base_playlist.uuid} | {self.name}'

    def save(self, *args, **kwargs):
        CriteriaPlaylist.objects.create(
            user=self.user,
            type=self.type,
            criteria=self.criteria,
            base_playlist=self.base_playlist
        )
