from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from bodzify_api.model.track.lib.LibraryTrack import UploadedTrack

from .SearchFilterSet import SearchFilterSet


class LibTrackSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = UploadedTrack
        search_fields = [LibTrackFields.TITLE]
