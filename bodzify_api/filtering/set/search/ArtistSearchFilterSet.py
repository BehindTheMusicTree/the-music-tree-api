from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.artist.Fields import Fields as ArtistFields

from .SearchFilterSet import SearchFilterSet


class ArtistSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = Artist
        search_fields = [ArtistFields.NAME_PUBLIC]
