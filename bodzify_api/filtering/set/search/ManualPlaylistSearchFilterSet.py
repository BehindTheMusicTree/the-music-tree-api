from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from .SearchFilterSet import SearchFilterSet


class ManualPlaylistSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = ManualPlaylist
        search_fields = [PlaylistFields.NAME_PUBLIC]