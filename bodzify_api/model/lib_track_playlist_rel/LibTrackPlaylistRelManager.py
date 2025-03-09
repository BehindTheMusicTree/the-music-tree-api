from typing import TYPE_CHECKING

from django.db.models import F

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.user.User import User

from .Fields import Fields


if TYPE_CHECKING:
    from .LibTrackPlaylistRel import LibTrackPlaylistRel


class LibTrackPlaylistRelManager(StandardResourceManager):

    def update_positions_to_fill_deleted_ones(self, playlist: Playlist):
        tracks_positions_ordered_asc = self.filter(playlist=playlist).order_by(Fields.POSITION)

        for i, relation in enumerate(tracks_positions_ordered_asc, 1):
            relation: LibTrackPlaylistRel = relation  # for type hinting
            relation.position = i
            relation.save()

    def delete_instance(self, user: User, playlist: Playlist, lib_track: LibraryTrack):
        lib_track_playlist_rel: LibTrackPlaylistRel = self.get(user=user, playlist=playlist, lib_track=lib_track)
        lib_track_playlist_rel.delete()
        lib_track_playlist_rels = self.filter(
            user=user, playlist=playlist, position__gt=lib_track_playlist_rel.position)
        lib_track_playlist_rels.update(position=F(Fields.POSITION) - 1)
