from typing import TYPE_CHECKING
from django.db import models
from django.db.models import QuerySet
from typing import Optional

from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from bodzify_api.model.criteria.Criteria import Criteria
    from .CriteriaPlaylist import CriteriaPlaylist
    from .CriterialessPlaylistNames import CriterialessPlaylistNames


class CriteriaPlaylistManager(StandardResourceManager):

    def get_by_name(self, user, name: str) -> Optional['CriteriaPlaylist']:
        return self.filter(user=user).filter(
            models.Q(criteria__name=name) |
            models.Q(criteria__isnull=True,
                     type__in=[models.Q(name=CriterialessPlaylistNames.GENRE) |
                               models.Q(name=CriterialessPlaylistNames.TAG)])
        ).first()

    def update_instance(self, instance: 'CriteriaPlaylist', **kwargs) -> 'CriteriaPlaylist':
        original_root = instance.root
        updated_instance: CriteriaPlaylist = super().update_instance(instance, **kwargs)
        if original_root != updated_instance.root:
            self.update_descendants_root(instance=updated_instance, root=updated_instance.root)
        return updated_instance

    def update_instance_and_children_root(self, instance: 'CriteriaPlaylist', root: 'CriteriaPlaylist'):
        instance.root = root
        instance.save(update_fields=[Fields.ROOT])
        self.update_descendants_root(instance=instance, root=root)

    def update_descendants_root(self, instance: 'CriteriaPlaylist', root: 'CriteriaPlaylist'):
        for child in instance.children.all():
            self.update_instance_and_children_root(instance=child, root=root)

    def update_ascendants_lib_tracks(self,
                                     instance: 'CriteriaPlaylist',
                                     old_parent: Optional['Criteria'],
                                     common_criteria: Optional['Criteria']):
        if instance.parent:
            self.add_lib_tracks_to_instance_and_ascendants_until_criteria_limit(
                instance=instance.parent,
                lib_tracks=instance.lib_tracks_not_archived.all(),
                criteria_limit=common_criteria)

        if old_parent:
            self.remove_lib_tracks_from_instance_and_ascendants_until_criteria_limit(
                instance=old_parent.criteria_playlist,
                lib_tracks=instance.lib_tracks_not_archived.all(),
                criteria_limit=common_criteria)

    def add_lib_tracks_to_instance_and_ascendants_until_criteria_limit(self,
                                                                       instance: 'CriteriaPlaylist',
                                                                       lib_tracks: QuerySet['LibraryTrack'],
                                                                       criteria_limit: Optional['Criteria'] = None):
        if instance.criteria != criteria_limit:
            from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
            for lib_track in lib_tracks:
                LibTrackPlaylistRel(user=instance.user, playlist=instance, library_track=lib_track).save()

            if instance.parent:
                self.add_lib_tracks_to_instance_and_ascendants_until_criteria_limit(instance=instance.parent,
                                                                                    lib_tracks=lib_tracks,
                                                                                    criteria_limit=criteria_limit)

    def remove_lib_tracks_from_instance_and_ascendants_until_criteria_limit(
            self, instance: 'CriteriaPlaylist',
            lib_tracks: QuerySet['LibraryTrack'],
            criteria_limit: Optional['Criteria'] = None):
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel

        if instance.criteria != criteria_limit:
            instance.lib_track_playlist_rels.filter(library_track__in=lib_tracks).delete()
            LibTrackPlaylistRel.objects.update_positions_to_fill_deleted_ones(instance)

            if instance.parent:
                self.remove_lib_tracks_from_instance_and_ascendants_until_criteria_limit(instance=instance.parent,
                                                                                         lib_tracks=lib_tracks,
                                                                                         criteria_limit=criteria_limit)
