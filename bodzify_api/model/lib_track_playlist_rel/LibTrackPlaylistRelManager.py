
from typing import TYPE_CHECKING, cast, Dict

from django.db.models import F

from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from bodzify_api.model.user.User import User

from .Fields import Fields


if TYPE_CHECKING:
    from .LibTrackPlaylistRel import LibTrackPlaylistRel
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from bodzify_api.model.playlist.Playlist import Playlist


class LibTrackPlaylistRelManager(StandardResourceManager):

    def _decrement_positions_of_following_tracks(self, playlist: 'Playlist', position: int):
        self.filter(
            user=playlist.user, playlist=playlist, position__gt=position
        ).update(
            position=F(Fields.POSITION) - 1)

    def _increment_positions_of_following_tracks(self, playlist: 'Playlist', position: int):
        self.filter(
            user=playlist.user, playlist=playlist, position__gte=position
        ).update(
            position=F(Fields.POSITION) + 1)

    def update_positions_to_fill_deleted_ones(self, playlist: 'Playlist'):
        tracks_positions_ordered_asc = self.filter(
            user=playlist.user, playlist=playlist
        ).exclude(
            position__isnull=True
        ).order_by(
            Fields.POSITION)

        for i, relation in enumerate(tracks_positions_ordered_asc, 1):
            relation: LibTrackPlaylistRel = relation  # for type hinting
            relation.position = i
            relation.save()

    def archive_instances_of_lib_track(self, lib_track: 'LibraryTrack'):
        for lib_track_playlist_rel in lib_track.lib_track_playlist_rels.all():
            lib_track_old_position = cast(int, lib_track_playlist_rel.position)  # Is not None before archiving
            lib_track_playlist_rel.position = None
            lib_track_playlist_rel.save(update_fields=[Fields.POSITION])

            self._decrement_positions_of_following_tracks(lib_track_playlist_rel.playlist, lib_track_old_position)

    def unarchive_instances_of_lib_track(self, lib_track: 'LibraryTrack'):
        for lib_track_playlist_rel in lib_track.lib_track_playlist_rels.all():
            self._increment_positions_of_following_tracks(lib_track_playlist_rel.playlist, 1)
            lib_track_playlist_rel.position = 1
            lib_track_playlist_rel.save(update_fields=[Fields.POSITION])

    def delete_instance(self, user: User, playlist: 'Playlist', lib_track: 'LibraryTrack'):
        from .LibTrackPlaylistRel import LibTrackPlaylistRel
        lib_track_playlist_rel: LibTrackPlaylistRel = self.get(user=user, playlist=playlist, lib_track=lib_track)
        if lib_track_playlist_rel.position is not None:  # if lib track not archived
            self._decrement_positions_of_following_tracks(playlist, lib_track_playlist_rel.position)
        lib_track_playlist_rel.delete()
