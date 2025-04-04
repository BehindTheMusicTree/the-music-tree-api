from typing import TYPE_CHECKING, cast

from django.db.models import F, QuerySet

from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from bodzify_api.model.user.User import User

from .Fields import Fields


if TYPE_CHECKING:
    from .LibTrackPlaylistRel import LibTrackPlaylistRel
    from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
    from bodzify_api.model.playlist.Playlist import Playlist


class LibTrackPlaylistRelManager(StandardResourceManager):

    def _decrement_positions_of_following_tracks(self, playlist: 'Playlist', position: int):
        self.filter(
            user=playlist.user, playlist=playlist, **{f'{Fields.POSITION}__gt': position}
        ).update(
            position=F(Fields.POSITION) - 1)

    def _increment_positions_of_following_tracks(self, playlist: 'Playlist', position: int):
        self.filter(
            user=playlist.user, playlist=playlist, **{f'{Fields.POSITION}__gte': position}
        ).update(
            position=F(Fields.POSITION) + 1)

    def update_positions_to_fill_deleted_ones(self, playlist: 'Playlist'):
        tracks_positions_ordered_asc = self.filter(
            user=playlist.user, playlist=playlist
        ).exclude(
            **{Fields.POSITION + '__isnull': True}
        ).order_by(
            Fields.POSITION)

        for i, relation in enumerate(tracks_positions_ordered_asc, 1):
            relation: LibTrackPlaylistRel = relation  # for type hinting
            relation.position = i
            relation.save(update_fields=[Fields.POSITION])

    def archive_instances_of_uploaded_track(self, uploaded_track: 'UploadedTrack'):
        for uploaded_track_playlist_rel in uploaded_track.uploaded_track_playlist_rels.all():
            uploaded_track_old_position = cast(
                int, uploaded_track_playlist_rel.position)  # Is not None before archiving
            uploaded_track_playlist_rel.position = None
            uploaded_track_playlist_rel.save(update_fields=[Fields.POSITION])

            self._decrement_positions_of_following_tracks(
                uploaded_track_playlist_rel.playlist, uploaded_track_old_position)

    def unarchive_instances_of_uploaded_track(self, uploaded_track: 'UploadedTrack'):
        for uploaded_track_playlist_rel in uploaded_track.uploaded_track_playlist_rels.all():
            self._increment_positions_of_following_tracks(uploaded_track_playlist_rel.playlist, 1)
            uploaded_track_playlist_rel.position = 1
            uploaded_track_playlist_rel.save(update_fields=[Fields.POSITION])

    def delete_instance(self, user: User, playlist: 'Playlist', uploaded_track: 'UploadedTrack'):
        from .LibTrackPlaylistRel import LibTrackPlaylistRel
        uploaded_track_playlist_rel: LibTrackPlaylistRel = self.get(
            user=user, playlist=playlist, uploaded_track=uploaded_track)
        if uploaded_track_playlist_rel.position is not None:  # if lib track not archived
            self._decrement_positions_of_following_tracks(playlist, uploaded_track_playlist_rel.position)
        uploaded_track_playlist_rel.delete()

    def move_tracks_to_playlist_beginning(
            self, source_rels: QuerySet['LibTrackPlaylistRel'], target_playlist: 'Playlist') -> None:
        from .Fields import Fields

        if not source_rels:
            return

        self.filter(
            user=target_playlist.user,
            playlist=target_playlist,
            position__isnull=False
        ).update(
            position=F(Fields.POSITION) + source_rels.count()
        )

        for i, relation in enumerate(source_rels.order_by(Fields.POSITION), 1):
            relation.playlist = target_playlist
            relation.position = i
            relation.save(update_fields=[Fields.POSITION, 'playlist'])

    def get_ordered_relations_for_playlist(self, playlist: 'Playlist') -> QuerySet['LibTrackPlaylistRel']:
        """
        Returns ordered relations for a playlist, with non-archived tracks first (sorted by position)
        followed by archived tracks (null positions).
        """
        return self.filter(
            user=playlist.user,
            playlist=playlist
        ).select_related('uploaded_track').order_by(
            F(Fields.POSITION).desc(nulls_last=True),
            Fields.POSITION
        )
