from typing import TYPE_CHECKING

from bodzify_api.model.public_standard_resource.PublicStandardResourceManager import PublicStandardResourceManager
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from .Fields import Fields

if TYPE_CHECKING:
    from .LibTrackPlaylistRel import LibTrackPlaylistRel


class LibTrackPlaylistRelManager(PublicStandardResourceManager):

    def update_positions_to_fill_deleted_ones(self, base_playlist: BasePlaylist):
        tracks_positions_ordered_asc = self.filter(base_playlist=base_playlist).order_by(Fields.POSITION)

        for i, relation in enumerate(tracks_positions_ordered_asc, 1):
            relation: LibTrackPlaylistRel = relation  # for type hinting
            relation.position = i
            relation.save()
