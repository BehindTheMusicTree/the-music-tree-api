from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.model.playlist.Fields import Fields as PlayListFields

from .SearchFilterSet import SearchFilterSet


class ManualPlaylistSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = ManualPlaylist
        search_fields = [PlayListFields.NAME_PUBLIC]
