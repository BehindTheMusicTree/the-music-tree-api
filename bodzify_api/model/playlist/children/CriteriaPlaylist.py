#!/usr/bin/env python

from django.db import models

from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabels as CriteriaAttributesLabels
from bodzify_api.model.criteria.CriteriaType import CriteriaType, CriteriaTypesId
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist, AttributesLabels as BasePlaylistAttributesLabels
from bodzify_api.model.playlist.children.BasePlaylistChild import BasePlaylistChild, \
    AttributesLabels as ChildAttributesLabels


class SpecialNames:
    GENRELESS = 'Genreless'
    TAGLESS = 'Tagless'


class TypesLabel:
    GENRE = 'genre'
    TAG = 'tag'


class AttributesLabels:
    BASE_PLAYLIST = ChildAttributesLabels.BASE_PLAYLIST
    UUID = ChildAttributesLabels.UUID
    USER = ChildAttributesLabels.USER
    CREATED_ON = ChildAttributesLabels.CREATED_ON
    UPDATED_ON = ChildAttributesLabels.UPDATED_ON
    LIB_TRACKS = ChildAttributesLabels.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = ChildAttributesLabels.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = ChildAttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ChildAttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ChildAttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildAttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = ChildAttributesLabels.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = ChildAttributesLabels.LAST_TRACK_LIST_UPDATE_DATE
    CRITERIA = 'criteria'
    TYPE = 'type'
    PARENT = 'parent'
    ROOT = 'root'
    NAME = 'name'


class CriteriaPlaylist(BasePlaylistChild):
    base_playlist = models.OneToOneField(BasePlaylist,
                                         on_delete=models.CASCADE,
                                         primary_key=True,
                                         related_name=BasePlaylistAttributesLabels.CRITERIA_PLAYLIST_CHILD)
    criteria = models.OneToOneField(Criteria,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    related_name=CriteriaAttributesLabels.CRITERIA_PLAYLIST)
    type = models.ForeignKey(CriteriaType, on_delete=models.CASCADE, blank=True, null=False)

    # null must be True because when the root is the criteria playlist itself, we must create it first with a null root
    # and then set the root to itself
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               related_name='child_playlist')
    root = models.ForeignKey('self',
                             on_delete=models.CASCADE,
                             null=True,
                             related_name='descendant_playlist')

    class Meta:
        db_table = 'bodzify_api_criteria_playlist'
        verbose_name = 'Criteria Playlist'
        verbose_name_plural = 'Criteria Playlists'

    @property
    def name(self):
        if self.criteria is None:
            if self.type.pk == CriteriaTypesId.GENRE:
                return SpecialNames.GENRELESS
            elif self.type.pk == CriteriaTypesId.TAG:
                return SpecialNames.TAGLESS
        else:
            return self.criteria.name

    def __str__(self) -> str:
        return f'{str(self.base_playlist.uuid)} {self.name}'

    def _set_parent(self):
        if self.criteria is None:
            self.parent = None
        elif self.criteria.parent is None:
            self.parent = None
        else:
            self.parent = self.criteria.parent.criteria_playlist  # type: ignore

    def _set_root(self):
        if self.criteria:
            self.root = self.criteria.root.criteria_playlist  # type: ignore
        else:
            self.root = self

    def _create(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._set_root()
        super().save(update_fields=[AttributesLabels.ROOT])

    def _update(self, old_criteria_playlist: 'CriteriaPlaylist', *args, **kwargs):
        super().save(*args, **kwargs)

        if self.criteria:
            if self.root.criteria != self.criteria.root:  # type: ignore
                self._set_root()
                super().save(update_fields=[AttributesLabels.ROOT])
                self._update_root_of_children(criteria_playlist=self, new_root=self.root)  # type: ignore

    def _update_root_of_children(self, criteria_playlist: 'CriteriaPlaylist', new_root: 'CriteriaPlaylist'):
        criteria_playlist.root = new_root  # type: ignore
        children = criteria_playlist.get_children()
        if children.exists():
            for child in children:
                child.root = new_root
                child.save()

    def get_children(self) -> models.QuerySet['CriteriaPlaylist']:
        return CriteriaPlaylist.objects.filter(parent=self)

    def save(self, *args, **kwargs):
        self._set_parent()
        try:
            old_criteria_playlist = CriteriaPlaylist.objects.get(base_playlist=self.base_playlist)
            self._update(old_criteria_playlist, *args, **kwargs)  # type: ignore
        except CriteriaPlaylist.DoesNotExist:
            self._create(*args, **kwargs)
