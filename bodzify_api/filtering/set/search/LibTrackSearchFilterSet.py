from bodzify_api.model.uploaded_track.Fields import Fields as LibTrackFields
from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack

from .SearchFilterSet import SearchFilterSet


class LibTrackSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = UploadedTrack
        search_fields = [LibTrackFields.TITLE]
