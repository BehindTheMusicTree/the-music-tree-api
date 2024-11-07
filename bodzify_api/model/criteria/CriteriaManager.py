from typing import Generic, Optional, TYPE_CHECKING, TypeVar
from django.db.models import QuerySet

from bodzify_api.model.base.utils.public_standard_resource.PublicStandardResourceManager \
    import PublicStandardResourceManager
from .type.CriteriaType import CriteriaType
from .Fields import Fields as ModelFields

if TYPE_CHECKING:
    from bodzify_api.model.user.User import User
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
    from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel, \
        Fields as LibTrackPlaylistPositionRelFields
    from .Criteria import Criteria

T = TypeVar('T', bound='Criteria')


class CriteriaManager(PublicStandardResourceManager['T'], Generic[T]):
    model: type['Criteria']

    def create_instance(self, type_pk: int, **kwargs) -> T:
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
        type = CriteriaType.objects.get(pk=type_pk)
        instance = self.create(type=type, **kwargs)
        CriteriaPlaylist.objects.create(user=instance.user, criteria=instance, type=type)
        self.update_ascendants_of_criteria_and_children(instance)
        return instance

    def update_instance(self, instance: T, **kwargs) -> T:
        from bodzify_api.model.criteria.Criteria import Fields as ModelFields
        old_root = instance.root
        old_parent = instance.parent
        old_name = instance.name

        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()

        if old_root != instance.root:
            instance.criteria_playlist.save()
            self.update_root_of_children(criteria=instance, new_root=instance.root)

        if old_parent != instance.parent:
            instance.root = instance.calculate_root_degree()
            instance.save(update_fields=[ModelFields.ROOT])

            self._update_playlists_of_ascendants(instance, old_parent)
            self.update_ascendants_of_criteria_and_children(instance)

            if instance.parent:
                instance.criteria_playlist.parent = instance.parent.criteria_playlist
            else:
                instance.criteria_playlist.parent = None
            instance.criteria_playlist.save()

        if old_name != instance.name:
            lib_tracks: list['LibraryTrack'] = list(instance.library_tracks)
            for lib_track in lib_tracks:
                lib_track.update_file_tags_from_lib_track_instance_values()

        return instance

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

    def _update_playlists_of_ascendants(self, criteria: T, old_parent: Optional[T]):
        from bodzify_api.model.criteria.Criteria import Criteria as CriteriaModel
        common_criteria = CriteriaModel.get_common_criteria(criteria, old_parent)
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

    def get_roots(self, user: 'User') -> QuerySet[T]:
        return self.filter(user=user, parent__isnull=True)

    def update_ascendants_of_criteria_and_children(self, criteria: T):
        from bodzify_api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel

        criteria.ascendants.clear()
        current_degree = 1
        current_parent = criteria.parent

        while current_parent:
            CriteriaLineageRel.objects.create(
                user=criteria.user,
                descendant=criteria,
                ascendant=current_parent,
                degree=current_degree
            )
            current_parent = current_parent.parent
            current_degree = current_degree + 1

        for child in self.filter(parent=criteria):
            self.update_ascendants_of_criteria_and_children(child)

    def update_root_of_children(self, criteria: T, new_root: T):
        children = criteria.children
        if children.exists():
            children.update(root=new_root)
            for child in children:
                self.update_root_of_children(child, new_root)

    def add_tracks_to_playlist_of_criteria_and_ascendants_until_criteria_limit(
            self,
            criteria: 'Criteria',
            lib_tracks: QuerySet['LibraryTrack'],
            criteria_limit: Optional[T] = None):
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
            self,
            criteria: T,
            lib_tracks: QuerySet['LibraryTrack'],
            criteria_limit: Optional[T] = None):
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
