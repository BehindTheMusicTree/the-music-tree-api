#!/usr/bin/env python

from typing import Optional, TYPE_CHECKING
from django.db import models
from django.db.models import QuerySet

if TYPE_CHECKING:
    from bodzify_api.model.user.User import User
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
    from bodzify_api.model.criteria.Criteria import Criteria
    from bodzify_api.model.criteria.CriteriaAscendantRel import CriteriaAscendantRel
    from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
    from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel, \
        Fields as LibTrackPlaylistPositionRelFields


class CriteriaManager(models.Manager['Criteria']):
    model: type['Criteria']

    def _update_playlists_of_ascendants(self, criteria: 'Criteria', old_parent: Optional['Criteria']):

        common_criteria = Criteria.get_common_criteria(criteria, old_parent)
        lib_tracks = LibraryTrack.objects.filter(
            lib_track_position_relations__base_playlist=criteria.criteria_playlist.base_playlist
        )

        if criteria.parent:
            self.add_tracks_to_playlist_of_criteria_and_ascendants_until_criteria_limit(
                criteria=criteria.parent,
                lib_tracks=lib_tracks,
                criteria_limit=common_criteria
            )

        if old_parent:
            self.remove_tracks_from_playlists_of_criteria_and_ascendants_until_criteria_limit(
                criteria=old_parent,
                lib_tracks=lib_tracks,
                criteria_limit=common_criteria
            )

    @staticmethod
    def update_playlist_positions_to_fill_deleted_positions(base_playlist: 'BasePlaylist'):

        tracks_positions_ordered_asc = (
            LibTrackPlaylistPositionRel.objects
            .filter(base_playlist=base_playlist)
            .order_by(LibTrackPlaylistPositionRelFields.POSITION)
        )

        for i, relation in enumerate(tracks_positions_ordered_asc, 1):
            relation.position = i
            relation.save()

    def get_roots(self, user: 'User') -> QuerySet['Criteria']:
        return self.filter(user=user, parent__isnull=True)

    def save(self, criteria: 'Criteria', *args, **kwargs):
        criteria.root = criteria.parent.root if criteria.parent else criteria

        try:
            old_criteria: Criteria = self.get(user=criteria.user, uuid=criteria.uuid)
            old_criteria_name = old_criteria.name
            self.update(criteria, old_criteria, *args, **kwargs)

            if old_criteria_name != criteria.name:
                criteria.library_tracks.all().update_file_tags()
        except self.model.DoesNotExist:
            self.create(criteria, *args, **kwargs)

    def create(self, criteria: 'Criteria', *args, **kwargs):
        models.Model.save(criteria, *args, **kwargs)

        CriteriaPlaylist.objects.create(
            user=criteria.user,
            type=criteria.type,
            criteria=criteria
        )
        self.update_ascendants_of_criteria_and_children(criteria)

    def update(self, criteria: 'Criteria', old_criteria: 'Criteria', *args, **kwargs):
        models.Model.save(criteria, *args, **kwargs)

        if old_criteria.root != criteria.root:
            criteria.criteria_playlist.save()
            self.update_root_of_children(criteria=criteria, new_root=criteria.root)

        if old_criteria.parent != criteria.parent:
            self._update_playlists_of_ascendants(criteria, old_criteria.parent)
            self.update_ascendants_of_criteria_and_children(criteria)

            if criteria.parent:
                criteria.criteria_playlist.parent = criteria.parent.criteria_playlist
            else:
                criteria.criteria_playlist.parent = None
            criteria.criteria_playlist.save()

    def update_ascendants_of_criteria_and_children(self, criteria: 'Criteria'):
        criteria.ascendants.clear()
        current_degree = 1
        current_parent = criteria.parent

        while current_parent:
            CriteriaAscendantRel.objects.create(
                user=criteria.user,
                descendant=criteria,
                ascendant=current_parent,
                degree=current_degree
            )
            current_parent = current_parent.parent
            current_degree = current_degree + 1

        for child in self.filter(parent=criteria):
            self.update_ascendants_of_criteria_and_children(child)

    def update_root_of_children(self, criteria: 'Criteria', new_root: 'Criteria'):
        children = criteria.children
        if children.exists():
            children.update(root=new_root)
            for child in children:
                self.update_root_of_children(child, new_root)

    def add_tracks_to_playlist_of_criteria_and_ascendants_until_criteria_limit(
            self, criteria: 'Criteria', lib_tracks: QuerySet['LibraryTrack'],
            criteria_limit: Optional['Criteria'] = None):
        if criteria != criteria_limit:
            base_playlist = criteria.criteria_playlist.base_playlist

            for lib_track in lib_tracks:
                LibTrackPlaylistPositionRel.objects.create(
                    user=criteria.user,
                    base_playlist=base_playlist,
                    library_track=lib_track
                )

            if criteria.parent:
                self.add_tracks_to_playlist_of_criteria_and_ascendants_until_criteria_limit(
                    criteria=criteria.parent,
                    lib_tracks=lib_tracks,
                    criteria_limit=criteria_limit
                )

    def remove_tracks_from_playlists_of_criteria_and_ascendants_until_criteria_limit(
            self, criteria: 'Criteria', lib_tracks: QuerySet['LibraryTrack'],
            criteria_limit: Optional['Criteria'] = None):
        if criteria != criteria_limit:
            base_playlist = criteria.criteria_playlist.base_playlist

            (LibTrackPlaylistPositionRel.objects
             .filter(base_playlist=base_playlist, library_track__in=lib_tracks)
             .delete())

            self.update_playlist_positions_to_fill_deleted_positions(base_playlist)

            if criteria.parent:
                self.remove_tracks_from_playlists_of_criteria_and_ascendants_until_criteria_limit(
                    criteria=criteria.parent,
                    lib_tracks=lib_tracks,
                    criteria_limit=criteria_limit
                )
