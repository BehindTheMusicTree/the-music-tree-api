from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from .SearchFilterSet import SearchFilterSet


class LibTrackSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = LibraryTrack
        search_fields = [LibTrackFields.TITLE]