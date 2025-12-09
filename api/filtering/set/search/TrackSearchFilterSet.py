from api.model.track.Fields import Fields as TrackFields
from api.model.track.Track import Track

from .SearchFilterSet import SearchFilterSet


class TrackSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = Track
        search_fields = [TrackFields.TITLE]

