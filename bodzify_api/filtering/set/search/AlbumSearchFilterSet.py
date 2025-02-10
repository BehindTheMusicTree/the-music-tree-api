from bodzify_api.model.album.Album import Album
from bodzify_api.model.album.Fields import Fields as AlbumFields
from .SearchFilterSet import SearchFilterSet


class AlbumSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = Album
        search_fields = [AlbumFields.NAME]