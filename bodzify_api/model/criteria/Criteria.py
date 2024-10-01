#!/usr/bin/env python

from typing import Optional
import shortuuid

from django.utils import timezone
from django.db import models
from django.db.models import QuerySet
from django.contrib.auth.models import User

from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api import settings


class AttributesLabel:
    MODEL = 'Criteria'
    UUID = 'uuid'
    USER = 'user'
    NAME = 'name'
    TYPE = 'type'
    PARENT = 'parent'
    ASCENDANT = 'ascendant'
    ASCENDANTS = ASCENDANT + 's'
    DESCENDANT = 'descendant'
    DESCENDANTS = DESCENDANT + 's'
    CRITERIA_ASCENDANT_RELATION_ASCENDANTS = 'criteria_ascendant_relation_ascendants'
    CRITERIA_ASCENDANT_RELATION_DESCENDANTS = 'criteria_ascendant_relation_descendants'
    CHILDREN = 'children'
    ROOT = 'root'
    CREATED_ON = 'created_on'
    LIB_TRACKS = 'library_tracks'
    CRITERIA_PLAYLIST = 'criteria_playlist'


class Criteria(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=settings.UUID_LEN, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=settings.CRITERIA_NAME_LEN_MAX, default=None)
    type = models.ForeignKey('CriteriaType', on_delete=models.CASCADE)
    parent = models.ForeignKey(AttributesLabel.MODEL,
                               on_delete=models.CASCADE, null=True,
                               related_name='child')
    ascendants = models.ManyToManyField(AttributesLabel.MODEL,
                                        through='CriteriaAscendantRelation',
                                        related_name=AttributesLabel.MODEL + 's')

    # null must be True because when the root is the criteria itself, we must create it first with a null root
    # and then set the root to itself
    root = models.ForeignKey(AttributesLabel.MODEL,
                             on_delete=models.CASCADE,
                             null=True,
                             related_name=AttributesLabel.DESCENDANT)
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        unique_together = (AttributesLabel.USER, AttributesLabel.NAME)
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name='criteria_non_empty_name')]

    @staticmethod
    def is_criteria1_descendant_of_criteria2(criteria1: 'Criteria', criteria2: 'Criteria'):
        if criteria1.parent == criteria2:
            return True
        elif criteria1.parent:
            return Criteria.is_criteria1_descendant_of_criteria2(criteria1.parent, criteria2)
        else:
            return False

    @ staticmethod
    def _update_playlist_positions_to_fill_deleted_positions(base_playlist: BasePlaylist):
        from bodzify_api.model.PlaylistLibTrackRelation \
            import PlaylistLibTrackRelation, AttributesLabel as PlaylistLibTrackRelationAttributesLabels
        tracks_positions_ordered_asc = (
            PlaylistLibTrackRelation.objects
            .filter(base_playlist=base_playlist)
            .order_by(PlaylistLibTrackRelationAttributesLabels.POSITION)
        )
        i = 1
        for relation in tracks_positions_ordered_asc:
            relation.position = i
            relation.save()
            i += 1

    @staticmethod
    def _update_ascendants_of_criteria_and_children(criteria: 'Criteria'):
        criteria.ascendants.clear()
        current_degree = 1
        current_parent = criteria.parent
        while current_parent:
            from bodzify_api.model.criteria.CriteriaAscendantRelation import CriteriaAscendantRelation
            CriteriaAscendantRelation.objects.create(descendant=criteria,
                                                     ascendant=current_parent,
                                                     degree=current_degree)
            current_parent = current_parent.parent
            current_degree = current_degree + 1

        for child in criteria.get_children():
            Criteria._update_ascendants_of_criteria_and_children(child)

    def __str__(self) -> str:
        return str(self.uuid) + " " + self.name

    def _create(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
        CriteriaPlaylist.objects.create(base_playlist=BasePlaylist.objects.create(user=self.user),
                                        type=self.type,
                                        criteria=self)
        Criteria._update_ascendants_of_criteria_and_children(self)

    def _update(self, old_criteria: 'Criteria', *args, **kwargs):
        super().save(*args, **kwargs)

        if old_criteria.root != self.root:
            self.criteria_playlist.save()  # type: ignore
            self._update_root_of_children(criteria=self, new_root=self.root)  # type: ignore

        if old_criteria.parent != self.parent:
            self._update_playlists_of_ascendants(old_criteria.parent)
            Criteria._update_ascendants_of_criteria_and_children(self)

            print("ICI")
            if self.parent is not None:
                print("PARENR")
                self.criteria_playlist.parent = self.parent.criteria_playlist  # type: ignore
            else:
                self.criteria_playlist.parent = None  # type: ignore
            self.criteria_playlist.save()  # type: ignore

    def _update_playlists_of_ascendants(self, old_parent: Optional['Criteria']):
        common_criteria = self.get_common_criteria(old_parent)

        from bodzify_api.model.track.LibraryTrack import LibraryTrack
        lib_tracks = LibraryTrack.objects.filter(
            playlist_lib_track_relations__base_playlist=self.criteria_playlist.base_playlist)  # type: ignore

        if self.parent is not None:
            self.parent._add_tracks_to_playlist_of_criteria_and_ascendants_until_criteria_limit(
                lib_tracks=lib_tracks,
                criteria_limit=common_criteria)

        if old_parent is not None:
            old_parent._remove_tracks_from_playlists_of_criteria_and_ascendants_until_criteria_limit(
                lib_tracks=lib_tracks,
                criteria_limit=common_criteria)

    def _add_tracks_to_playlist_of_criteria_and_ascendants_until_criteria_limit(
            self, lib_tracks: QuerySet, criteria_limit: Optional['Criteria'] = None):
        if self != criteria_limit:
            base_playlist = self.criteria_playlist.base_playlist  # type: ignore

            from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
            for lib_track in lib_tracks:
                PlaylistLibTrackRelation.objects.create(base_playlist=base_playlist, library_track=lib_track)
            if self.parent is not None:
                self.parent._add_tracks_to_playlist_of_criteria_and_ascendants_until_criteria_limit(
                    lib_tracks=lib_tracks,
                    criteria_limit=criteria_limit)

    @ staticmethod
    def _remove_tracks_from_playlist(base_playlist: BasePlaylist, lib_tracks: QuerySet):
        from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
        (
            PlaylistLibTrackRelation.objects
            .filter(base_playlist=base_playlist, library_track__in=lib_tracks)  # type: ignore
            .delete()
        )

    def _remove_tracks_from_playlists_of_criteria_and_ascendants_until_criteria_limit(
            self, lib_tracks: QuerySet, criteria_limit: Optional['Criteria'] = None):
        if self != criteria_limit:
            Criteria._remove_tracks_from_playlist(
                base_playlist=self.criteria_playlist.base_playlist, lib_tracks=lib_tracks)  # type: ignore
            Criteria._update_playlist_positions_to_fill_deleted_positions(
                self.criteria_playlist.base_playlist)  # type: ignore
            if self.parent is not None:
                self.parent._remove_tracks_from_playlists_of_criteria_and_ascendants_until_criteria_limit(
                    lib_tracks=lib_tracks,
                    criteria_limit=criteria_limit)

    def _update_root_of_children(self, criteria: 'Criteria', new_root: 'Criteria'):
        children = criteria.get_children()
        if children.exists():
            for child in children:
                child.root = new_root
                child.save()

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
        return Criteria.is_criteria1_descendant_of_criteria2(self, other_criteria)

    def get_children(self) -> QuerySet['Criteria']:
        return Criteria.objects.filter(parent=self)

    def save(self, *args, **kwargs):
        self.root = self.parent.root if self.parent else self
        try:
            old_criteria = Criteria.objects.get(uuid=self.uuid)
            self._update(old_criteria, *args, **kwargs)
        except Criteria.DoesNotExist:
            self._create(*args, **kwargs)
