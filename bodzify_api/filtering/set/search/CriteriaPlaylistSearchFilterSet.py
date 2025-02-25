from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import \
    CriteriaPlaylist

from .SearchFilterSet import SearchFilterSet


class CriteriaPlaylistSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = CriteriaPlaylist
        search_fields = ['criteria__name']  # Related field search