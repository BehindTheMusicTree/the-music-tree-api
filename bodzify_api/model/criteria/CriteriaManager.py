from typing import TYPE_CHECKING, TypeVar

from django.db import transaction
from django.db.models import QuerySet

from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields
from bodzify_api.model.lib_track_mixin.LibTrackMixinWithInternalNameManager import LibTrackMixinWithInternalNameManager

from .Fields import Fields
from .type.CriteriaType import CriteriaType


if TYPE_CHECKING:
    from bodzify_api.model.user.User import User
    from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
    from bodzify_api.model.playlist.Fields import Fields as PlaylistFields

    from .Criteria import Criteria

T = TypeVar('T', bound='Criteria')


class CriteriaManager(LibTrackMixinWithInternalNameManager[T]):
    model: type[T]

    def _refresh_ascendants_of_instance(self, instance: T):
        from .lineage_rel.CriteriaLineageRel import CriteriaLineageRel

        instance.ascendants_rels.all().delete()
        current_degree = 1
        current_parent = instance.parent

        while current_parent:
            CriteriaLineageRel.objects.create(
                user=instance.user, descendant=instance, ascendant=current_parent, degree=current_degree)
            current_parent = current_parent.parent
            current_degree = current_degree + 1

    def _refresh_ascendants_of_instance_and_children(self, instance):
        self._refresh_ascendants_of_instance(instance)
        for child in self.filter(parent=instance):
            self._refresh_ascendants_of_instance_and_children(child)

    def _refresh_ascendants_of_descendants(self, instance):
        for child in instance.children.all():
            self._refresh_ascendants_of_instance_and_children(child)

    def get_default_ordering(self) -> list[str]:
        return [LibTrackMixinFields.NAME_INTERNAL]

    def create(self, type_id: int, **kwargs) -> T:
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
        type = CriteriaType.objects.get(pk=type_id)
        instance: T = super().create(type=type, **kwargs)
        CriteriaPlaylist.objects.create(user=instance.user, criteria=instance, type=type)
        self._refresh_ascendants_of_instance(instance)
        return instance

    def update_instance(self, instance: T, **kwargs) -> T:
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
        old_root = instance.root
        old_parent = instance.parent
        old_name = instance.name

        updated_instance: T = super().update_instance(instance, **kwargs)

        if old_parent != updated_instance.parent:
            self._refresh_ascendants_of_instance_and_children(updated_instance)

            playlist_parent = updated_instance.parent.criteria_playlist if updated_instance.parent else None
            CriteriaPlaylist.objects.update_instance(instance=instance.criteria_playlist,
                                                     **{Fields.PARENT: playlist_parent})

            common_criteria = self.get_common_ascendant(updated_instance, old_parent)
            CriteriaPlaylist.objects.update_ascendants_lib_tracks(instance=updated_instance.criteria_playlist,
                                                                  old_parent=old_parent,
                                                                  common_criteria=common_criteria)

            if old_root != updated_instance.root:
                self.update_children_root(criteria=updated_instance, new_root=updated_instance.root)
                CriteriaPlaylist.objects.update_instance_and_children_root(instance=updated_instance.criteria_playlist,
                                                                           root=updated_instance.root.criteria_playlist)

        if old_name != updated_instance.name and updated_instance.lib_tracks:
            for lib_track in updated_instance.lib_tracks.all():
                lib_track.update_file_metadata_from_lib_track_instance_values()

        return updated_instance

    def get_common_ascendant(
            self, criteria_a: 'Criteria | None', criteria_b: 'Criteria | None') -> 'Criteria | None':
        if not criteria_a or not criteria_b:
            return None

        visited = set()
        current = criteria_a
        while current:
            visited.add(current)
            current = current.parent

        current = criteria_b
        while current:
            if current in visited:
                return current
            current = current.parent

        return None

    def get_all_descendants(self, criteria: 'Criteria') -> list:
        """
        Recursively get all descendants of a criteria.

        Args:
            criteria: The criteria whose descendants to retrieve

        Returns:
            A list of all descendant criteria
        """
        result = []
        for child in criteria.children.all():
            result.append(child)
            result.extend(self.get_all_descendants(child))
        return result

    def delete_instance(self, instance: T) -> None:
        """
        Delete a criteria and handle relationships.

        When deleting a criteria:
        - If it has children and a parent, children are reassigned to the parent
        - If it has children but no parent, children become root criteria
        - If it's a root criteria, tracks are moved to the criterialess playlist
        """
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        with transaction.atomic():
            from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields

            criteria_lib_tracks = instance.lib_tracks.all()
            for lib_track in criteria_lib_tracks:
                lib_track.genre = instance.parent
                lib_track.save(update_fields=[f'{LibTrackFields.GENRE}_id'])
                lib_track.update_file_metadata_from_lib_track_instance_values()

            if instance.is_root:
                CriteriaPlaylist.objects.transfer_direct_tracks_to_criterialess_playlist(
                    direct_tracks=criteria_lib_tracks,
                    criteria_playlist=instance.criteria_playlist)

            if instance.children.exists():
                children = list(instance.children.all())

                for child in children:
                    child.parent = instance.parent
                    child.save(update_fields=[f'{Fields.PARENT}_id'])
                    self._refresh_ascendants_of_instance_and_children(child)

                    child.criteria_playlist.parent = instance.parent.criteria_playlist if instance.parent else None
                    child.criteria_playlist.save(update_fields=[Fields.PARENT])

                    if not instance.parent:
                        CriteriaPlaylist.objects.make_playlist_root(child.criteria_playlist)

            # Delete the criteria instance directly
            # This will cascade delete its playlist due to foreign key relationships
            instance.delete()

    def get_roots(self, user: 'User') -> 'QuerySet[T]':
        return self.filter(user=user, parent__isnull=True)

    def update_children_root(self, criteria: 'Criteria', new_root: 'Criteria'):
        children = criteria.children.all()
        if children.exists():
            children.update(root=new_root)
            for child in children:
                self.update_children_root(child, new_root)
