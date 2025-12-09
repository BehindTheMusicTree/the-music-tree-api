from typing import TYPE_CHECKING

from django.db import models
from django.db.models import QuerySet

from api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from .Fields import Fields


if TYPE_CHECKING:
    from api.model.criteria.Criteria import Criteria
    from api.model.track.Track import Track

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

    def update_ascendants_tracks(
            self, instance: 'CriteriaPlaylist', old_parent: 'Criteria | None', common_criteria: 'Criteria | None'):
        if instance.parent:
            self.add_tracks_to_instance_and_ascendants_until_criteria_limit(
                instance=instance.parent, tracks=instance.tracks.all(), criteria_limit=common_criteria)

        if old_parent:
            self.remove_tracks_from_instance_and_ascendants_until_criteria_limit(
                instance=old_parent.criteria_playlist, tracks=instance.tracks.all(), criteria_limit=common_criteria)

    def add_tracks_to_instance_and_ascendants_until_criteria_limit(self,
                                                                   instance: 'CriteriaPlaylist',
                                                                   tracks: QuerySet['Track'],
                                                                   criteria_limit: 'Criteria | None' = None):
        if instance.criteria != criteria_limit:
            from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
            for track in tracks:
                TrackPlaylistRel(user=instance.user, playlist=instance, track=track).save()

            if instance.parent:
                self.add_tracks_to_instance_and_ascendants_until_criteria_limit(
                    instance=instance.parent, tracks=tracks, criteria_limit=criteria_limit)

    def remove_tracks_from_instance_and_ascendants_until_criteria_limit(
            self, instance: 'CriteriaPlaylist',
            tracks: QuerySet['Track'],
            criteria_limit: 'Criteria | None' = None):
        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

        if instance.criteria != criteria_limit:
            instance.track_playlist_rels.filter(track__in=tracks).delete()
            TrackPlaylistRel.objects.update_positions_to_fill_deleted_ones(instance)

            if instance.parent:
                self.remove_tracks_from_instance_and_ascendants_until_criteria_limit(
                    instance=instance.parent, tracks=tracks, criteria_limit=criteria_limit)

    def transfer_direct_tracks_to_criterialess_playlist(
            self, direct_tracks: QuerySet['Track'],
            criteria_playlist: 'CriteriaPlaylist'):
        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

        criterialess_playlist = self.get(
            user=criteria_playlist.user, criteria=None, type=criteria_playlist.type)

        direct_tracks_rels_in_criteria_playlist = criteria_playlist.track_playlist_rels.filter(
            track__uuid__in=[track.uuid for track in direct_tracks]
        )

        direct_tracks_rels_not_archived = direct_tracks_rels_in_criteria_playlist.filter(position__isnull=False)

        TrackPlaylistRel.objects.move_tracks_to_playlist_beginning(
            source_rels=direct_tracks_rels_not_archived, target_playlist=criterialess_playlist)

        direct_tracks_rels_in_criteria_playlist.filter(position__isnull=True).update(playlist=criterialess_playlist)

    def make_playlist_root(self, playlist: 'CriteriaPlaylist'):
        playlist.parent = None
        playlist.root = playlist
        playlist.save(update_fields=[Fields.PARENT, Fields.ROOT])

        # Update all descendant playlists to use this as the root
        self.update_descendants_root(instance=playlist, root=playlist)
