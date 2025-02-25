from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated

from bodzify_api.filtering.set.search.AlbumSearchFilterSet import \
    AlbumSearchFilterSet
from bodzify_api.filtering.set.search.ArtistSearchFilterSet import \
    ArtistSearchFilterSet
from bodzify_api.filtering.set.search.CriteriaPlaylistSearchFilterSet import \
    CriteriaPlaylistSearchFilterSet
from bodzify_api.filtering.set.search.LibTrackSearchFilterSet import \
    LibTrackSearchFilterSet
from bodzify_api.filtering.set.search.ManualPlaylistSearchFilterSet import \
    ManualPlaylistSearchFilterSet
from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.children.criteria.CriterialessPlaylistNames import \
    CriterialessPlaylistNames
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import \
    CriteriaPlaylist
from bodzify_api.model.playlist.children.manual.ManualPlaylist import \
    ManualPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.model.album.minimum import AlbumMinimumSerializer
from bodzify_api.serializer.model.artist.simple import ArtistSimpleSerializer
from bodzify_api.serializer.model.lib_track.output.detailed import \
    LibTrackDetailedSerializer
from bodzify_api.serializer.model.playlist.children.criteria.output.simple import \
    CriteriaSimpleSerializer
from bodzify_api.serializer.model.playlist.children.manual.output.simple import \
    ManualPlaylistSimpleSerializer

from ..pagination.DefaultMultipleModelLimitOffsetPagination import \
    DefaultMultipleModelLimitOffsetPagination


def is_string1_part_of_string2_regardless_of_case(string1: str, string2: str) -> bool:
    """
    Check if string1 is a substring of string2, ignoring case.
    Used for case-insensitive matching in criterialess playlist handling.
    """
    return string1.lower() in string2.lower()


class SearchViewSet(ObjectMultipleModelAPIViewSet):
    """
    ViewSet for searching across multiple models (tracks, albums, artists, and playlists).
    Uses model-specific filtersets to handle filtering for each model type.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultMultipleModelLimitOffsetPagination

    # Only used by drf spectacular to generate the schema
    def get_detailed_serializer_class(self):
        return LibTrackDetailedSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='query',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Search query string to filter results'
            )
        ],
        description=("""
            Search within tracks, albums, artists and playlists.
            The results is a set of four sets:
                - Playlist (searched and ordered by name);
                - Artist (searched and ordered by name);
                - Album (searched and ordered by name);
                - LibraryTrack (searched and ordered by title).
            """)
    )
    def get_querylist(self):
        user = self.request.user
        query = self.request.query_params.get('query', '')

        # Base querysets filtered by user
        lib_track_qs = LibraryTrack.objects.filter(user=user)
        manual_playlist_qs = ManualPlaylist.objects.filter(user=user)
        criteria_playlist_qs = CriteriaPlaylist.objects.filter(user=user)
        album_qs = Album.objects.filter(user=user)
        artist_qs = Artist.objects.filter(user=user)

        # Apply filtersets
        lib_track_fs = LibTrackSearchFilterSet(
            data=self.request.query_params,
            queryset=lib_track_qs
        )
        manual_playlist_fs = ManualPlaylistSearchFilterSet(
            data=self.request.query_params,
            queryset=manual_playlist_qs
        )
        criteria_playlist_fs = CriteriaPlaylistSearchFilterSet(
            data=self.request.query_params,
            queryset=criteria_playlist_qs
        )
        album_fs = AlbumSearchFilterSet(
            data=self.request.query_params,
            queryset=album_qs
        )
        artist_fs = ArtistSearchFilterSet(
            data=self.request.query_params,
            queryset=artist_qs
        )

        # Special handling for criterialess playlists
        criteria_playlist_qs = criteria_playlist_fs.qs
        if query:
            if is_string1_part_of_string2_regardless_of_case(query, CriterialessPlaylistNames.GENRE):
                criteria_playlist_qs = criteria_playlist_qs | criteria_playlist_qs.model.objects.filter(
                    user=user,
                    criteria__isnull=True,
                    type_pk=CriteriaTypePks.GENRE
                )
            if is_string1_part_of_string2_regardless_of_case(query, CriterialessPlaylistNames.TAG):
                criteria_playlist_qs = criteria_playlist_qs | criteria_playlist_qs.model.objects.filter(
                    user=user,
                    criteria__isnull=True,
                    type_pk=CriteriaTypePks.TAG
                )

        querylist = (
            {
                'queryset': lib_track_fs.qs,
                'serializer_class': LibTrackDetailedSerializer,
            },
            {
                'queryset': manual_playlist_fs.qs,
                'serializer_class': ManualPlaylistSimpleSerializer,
            },
            {
                'queryset': criteria_playlist_qs,
                'serializer_class': CriteriaSimpleSerializer,
            },
            {
                'queryset': album_fs.qs,
                'serializer_class': AlbumMinimumSerializer,
            },
            {
                'queryset': artist_fs.qs,
                'serializer_class': ArtistSimpleSerializer,
            })

        return querylist
