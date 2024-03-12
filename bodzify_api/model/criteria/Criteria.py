#!/usr/bin/env python

import logging
from typing import Optional
import shortuuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet
from bodzify_api.model.playlist.Playlist import Playlist
import bodzify_api.settings as settings

logger = logging.getLogger('bodzify_api')


class ATTRIBUTES_LABEL:
    UUID = "uuid"
    USER = "user"
    NAME = "name"
    TYPE = "type"
    PARENT = "parent"
    CHILDREN = "children"
    ROOT = "root"
    ADDED_ON = "added_on"


class Criteria(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=settings.CRITERIA_NAME_LENGTH_MAX, default=None)
    type = models.ForeignKey('bodzify_api.CriteriaType', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='child_criteria')
    root = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='descendant_criteria')
    added_on = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = (ATTRIBUTES_LABEL.USER, ATTRIBUTES_LABEL.NAME)
        constraints = [
            models.CheckConstraint(check=~models.Q(
                name=""), name="criteria_non_empty_name")
        ]

    def __str__(self) -> str:
        return str(self.uuid) + " " + self.name

    def save(self, *args, **kwargs):
        self.root = self.parent.root if self.parent else self
        try:
            old_criteria = Criteria.objects.get(uuid=self.uuid)
            self._update(old_criteria, *args, **kwargs)

        except Criteria.DoesNotExist:
            self._create(*args, **kwargs)

    def _create(self, *args, **kwargs):

        super().save(*args, **kwargs)
        from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
        CriteriaPlaylist(playlist=Playlist.objects.create(user=self.user), type=self.type, criteria=self).save()

    def _update(self, old_criteria: 'Criteria', *args, **kwargs):
        super().save(*args, **kwargs)

        if old_criteria.root != self.root:
            self._update_root_of_children(criteria=self, new_root=self.root)

        if old_criteria.parent != self.parent:
            self._update_playlists(old_criteria.parent)

    def _update_playlists(self, old_parent: Optional['Criteria']):
        common_criteria = self.get_common_criteria(old_parent)

        from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
        criteria_tracks = CriteriaPlaylist.objects.get(criteria=self).playlist.library_tracks.all()

        if self.parent is not None:
            self._add_tracks_to_playlist_of_criteria_and_ascendants_until_criteria_limit(
                criteria=self.parent,
                tracks=criteria_tracks,
                criteria_limit=common_criteria)

        if old_parent is not None:
            self._remove_tracks_from_playlists_of_criteria_and_ascendants_until_criteria_limit(
                criteria=old_parent,
                tracks=criteria_tracks,
                criteria_limit=common_criteria)

    def _add_tracks_to_playlist_of_criteria_and_ascendants_until_criteria_limit(
            self, criteria: 'Criteria', tracks: QuerySet, criteria_limit: Optional['Criteria'] = None):
        if criteria != criteria_limit:
            from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
            CriteriaPlaylist.objects.get(criteria=criteria).playlist.library_tracks.add(*tracks)
            if criteria.parent is not None:
                self._add_tracks_to_playlist_of_criteria_and_ascendants_until_criteria_limit(
                    criteria=criteria.parent,
                    tracks=tracks,
                    criteria_limit=criteria_limit)

    def _remove_tracks_from_playlists_of_criteria_and_ascendants_until_criteria_limit(
            self, criteria: 'Criteria', tracks: QuerySet, criteria_limit: Optional['Criteria'] = None):
        if criteria != criteria_limit:
            from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
            CriteriaPlaylist.objects.get(criteria=criteria).playlist.library_tracks.remove(*tracks)
            if criteria.parent is not None:
                self._remove_tracks_from_playlists_of_criteria_and_ascendants_until_criteria_limit(
                    criteria=criteria.parent,
                    tracks=tracks,
                    criteria_limit=criteria_limit)

    def get_common_criteria(self, criteriaB):
        visited = set()

        criteriaATreeItem = self
        while criteriaATreeItem is not None:
            visited.add(criteriaATreeItem)
            criteriaATreeItem = criteriaATreeItem.parent

        criteriaBTreeItem = criteriaB
        while criteriaBTreeItem is not None:
            if criteriaBTreeItem in visited:
                return criteriaBTreeItem
            criteriaBTreeItem = criteriaBTreeItem.parent

        return None

    def is_descendant_of(self, other_criteria):
        return self.is_criteria1_descendant_of_criteria2(self, other_criteria)

    def is_criteria1_descendant_of_criteria2(self, criteria1: 'Criteria', criteria2: 'Criteria'):
        if criteria1.parent == criteria2:
            return True
        elif criteria1.parent:
            return self.is_criteria1_descendant_of_criteria2(criteria1.parent, criteria2)
        else:
            return False

    def get_children(self):
        return Criteria.objects.filter(parent=self)

    def _update_root_of_children(self, criteria: 'Criteria', new_root: 'Criteria'):
        criteria.root = new_root  # type: ignore
        children = criteria.get_children()
        if children.exists():
            for child in children:
                child.root = new_root
                child.save()
