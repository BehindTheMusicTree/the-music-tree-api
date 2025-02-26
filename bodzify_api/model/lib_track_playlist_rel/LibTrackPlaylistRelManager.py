from typing import TYPE_CHECKING

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager

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
