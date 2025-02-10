from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from .SearchFilterSet import SearchFilterSet


class LibTrackSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = LibraryTrack
        search_fields = [LibTrackFields.TITLE]


class ManualPlaylistSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = ManualPlaylist
        search_fields = [PlaylistFields.NAME_PUBLIC]


class CriteriaPlaylistSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = CriteriaPlaylist
        search_fields = ['criteria__name']  # Special case for related field


class AlbumSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = Album
        search_fields = [AlbumFields.NAME]


class ArtistSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = Artist
        search_fields = [ArtistFields.NAME]