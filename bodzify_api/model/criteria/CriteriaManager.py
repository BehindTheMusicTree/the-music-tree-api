from typing import Generic, Optional, TYPE_CHECKING, TypeVar

from django.db.models import QuerySet

from bodzify_api.model.lib_track_mixin.LibTrackMixinManager import LibTrackMixinManager
from .type.CriteriaType import CriteriaType

if TYPE_CHECKING:
    from bodzify_api.model.user.User import User
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
    from .Criteria import Criteria

T = TypeVar('T', bound='Criteria')


class CriteriaManager(LibTrackMixinManager[T], Generic[T]):
    model: T

    def create_single(self, type_pk: int, **kwargs) -> T:
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
        type = CriteriaType.objects.get(pk=type_pk)
        instance = self.create(type=type, **kwargs)
        CriteriaPlaylist.objects.create(user=instance.user, criteria=instance, type=type)
        self.update_ascendants_of_criteria_and_children(instance)
        return instance

    def update_single(self, instance: T, **kwargs) -> T:
        from bodzify_api.model.criteria.Criteria import Fields as ModelFields
        old_root = instance.root
        old_parent = instance.parent
        old_name = instance.name

        instance.save(**kwargs)

        if old_parent != instance.parent:
            instance.save(update_fields=[ModelFields.ROOT])

            common_criteria = self.get_common_ascendant(instance, old_parent)
            CriteriaPlaylist.objects.update_ascendants_tracks(instance=instance.criteria_playlist,
                                                              old_parent=old_parent,
                                                              common_criteria=common_criteria)
            self.update_ascendants_of_criteria_and_children(instance)

            playlist_parent = instance.parent.criteria_playlist if instance.parent else None
            CriteriaPlaylist.objects.update_single(instance=instance.criteria_playlist, parent=playlist_parent)

            if old_root != instance.root:
                self.update_children_root(criteria=instance, new_root=instance.root)
                CriteriaPlaylist.objects.update_instance_and_children_root(instance=instance.criteria_playlist,
                                                                           root=instance.root.criteria_playlist)

        if old_name != instance.name:
            lib_tracks: list['LibraryTrack'] = list(instance.library_tracks)
            for lib_track in lib_tracks:
                lib_track.update_file_tags_from_lib_track_instance_values()

        return instance

    def get_common_ascendant(
            self, criteria_a: Optional['Criteria'], criteria_b: Optional['Criteria']) -> Optional['Criteria']:
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

    def get_roots(self, user: 'User') -> QuerySet[T]:
        return self.filter(user=user, parent__isnull=True)

    def update_ascendants_of_criteria_and_children(self, criteria: T):
        from bodzify_api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel

        criteria.ascendants.clear()
        current_degree = 1
        current_parent = criteria.parent

        while current_parent:
            CriteriaLineageRel.objects.create(user=criteria.user,
                                              descendant=criteria,
                                              ascendant=current_parent,
                                              degree=current_degree)
            current_parent = current_parent.parent
            current_degree = current_degree + 1

        for child in self.filter(parent=criteria):
            self.update_ascendants_of_criteria_and_children(child)

    def update_children_root(self, criteria: 'Criteria', new_root: 'Criteria'):
        children = criteria.children.all()
        if children.exists():
            children.update(root=new_root)
            for child in children:
                self.update_children_root(child, new_root)
