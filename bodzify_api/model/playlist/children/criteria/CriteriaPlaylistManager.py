from typing import TYPE_CHECKING

from django.db import models
from django.db.models import QuerySet

from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager

from .Fields import Fields


if TYPE_CHECKING:
    from bodzify_api.model.criteria.Criteria import Criteria
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

    from .CriterialessPlaylistNames import CriterialessPlaylistNames
    from .CriteriaPlaylist import CriteriaPlaylist


class CriteriaPlaylistManager(StandardResourceManager):

    def get_by_name(self, user, name: str) -> 'CriteriaPlaylist | None':
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

    def update_ascendants_lib_tracks(
            self, instance: 'CriteriaPlaylist', old_parent: 'Criteria | None', common_criteria: 'Criteria | None'):
        if instance.parent:
            self.add_lib_tracks_to_instance_and_ascendants_until_criteria_limit(
                instance=instance.parent, lib_tracks=instance.lib_tracks.all(), criteria_limit=common_criteria)

        if old_parent:
            self.remove_lib_tracks_from_instance_and_ascendants_until_criteria_limit(
                instance=old_parent.criteria_playlist, lib_tracks=instance.lib_tracks.all(), criteria_limit=common_criteria)

    def add_lib_tracks_to_instance_and_ascendants_until_criteria_limit(self,
                                                                       instance: 'CriteriaPlaylist',
                                                                       lib_tracks: QuerySet['LibraryTrack'],
                                                                       criteria_limit: 'Criteria | None' = None):
        if instance.criteria != criteria_limit:
            from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
            for lib_track in lib_tracks:
                LibTrackPlaylistRel(user=instance.user, playlist=instance, lib_track=lib_track).save()

            if instance.parent:
                self.add_lib_tracks_to_instance_and_ascendants_until_criteria_limit(
                    instance=instance.parent, lib_tracks=lib_tracks, criteria_limit=criteria_limit)

    def remove_lib_tracks_from_instance_and_ascendants_until_criteria_limit(
            self, instance: 'CriteriaPlaylist',
            lib_tracks: QuerySet['LibraryTrack'],
            criteria_limit: 'Criteria | None' = None):
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel

        if instance.criteria != criteria_limit:
            instance.lib_track_playlist_rels.filter(lib_track__in=lib_tracks).delete()
            LibTrackPlaylistRel.objects.update_positions_to_fill_deleted_ones(instance)

            if instance.parent:
                self.remove_lib_tracks_from_instance_and_ascendants_until_criteria_limit(
                    instance=instance.parent, lib_tracks=lib_tracks, criteria_limit=criteria_limit)

    def transfer_direct_tracks_to_criterialess_playlist(
            self, criteria_playlist: 'CriteriaPlaylist', criteria: 'Criteria'):
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        from bodzify_api.model.lib_track_playlist_rel.Fields import Fields as LibTrackPlaylistRelFields

        # Get the criterialess playlist for this criteria type
        criterialess_playlist = self.get(
            user=criteria_playlist.user,
            criteria=None,
            type=criteria_playlist.type
        )

        # Get pre-filtered and ordered tracks to move
        source_rels = list(LibTrackPlaylistRel.objects.filter(
            playlist=criteria_playlist,
            lib_track__genre=criteria
        ).select_related('lib_track').order_by(LibTrackPlaylistRelFields.POSITION))

        # Use the LibTrackPlaylistRelManager to move tracks
        LibTrackPlaylistRel.objects.move_tracks_to_playlist_beginning(
            source_rels=source_rels,
            target_playlist=criterialess_playlist,
            user=criteria_playlist.user
        )

    def ensure_tracks_in_parent_playlist(
            self, criteria_list: list['Criteria'],
            parent_playlist: 'CriteriaPlaylist', user):
        """
        Ensure all tracks from the given criteria list have relationships to the parent playlist.

        Args:
            criteria_list: List of criteria whose tracks need to be in the parent playlist
            parent_playlist: The parent playlist to ensure the tracks are in
            user: The user who owns the playlists and tracks
        """
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel

        # Get all criteria IDs
        all_criteria_ids = [c.pk for c in criteria_list]

        # Find all tracks from these criteria
        all_tracks = list(LibraryTrack.objects.filter(genre_id__in=all_criteria_ids).all())

        # For each track, create a relationship to the parent playlist if it doesn't exist
        for track in all_tracks:
            # This ensures tracks remain visible in parent playlists after deletion
            LibTrackPlaylistRel.objects.get_or_create(
                user=user,
                playlist=parent_playlist,
                lib_track=track
            )

    def make_playlist_root(self, playlist: 'CriteriaPlaylist'):
        """
        Set a playlist as its own root and update all descendants.

        Args:
            playlist: The playlist to make a root
        """
        playlist.parent = None
        playlist.root = playlist
        playlist.save(update_fields=[Fields.PARENT, Fields.ROOT])

        # Update all descendant playlists to use this as the root
        self.update_descendants_root(instance=playlist, root=playlist)
