from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from bodzify_api.filter.set.search.Fields import Fields as QueryFields
from bodzify_api.model.album.Album import Album
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.criteria.CriterialessPlaylistNames \
    import CriterialessPlaylistNames
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from bodzify_api.serializer.schema.model.album.minimum import AlbumMinimumSerializer
from bodzify_api.serializer.schema.model.artist.simple import ArtistSimpleSerializer
from bodzify_api.serializer.schema.model.playlist.children.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.schema.model.playlist.children.manual.output.simple import ManualPlaylistSimpleSerializer
from bodzify_api.serializer.schema.model.lib_track.output.detailed import LibTrackDetailedSerializer
from ..pagination.DefaultMultipleModelLimitOffsetPagination import DefaultMultipleModelLimitOffsetPagination


class QueryFiltersFields:
    TITLE = "title"
    ARTIST_NAME = "artist_name"
    ALBUM_NAME = "album_name"
    YEAR = "year"
    GENRE_NAME = "genre_name"
    TAG_NAME = "tag_name"
    PLAYLIST_NAME = "playlist_name"


class QueryFieldTypeValues:
    TITLE = QueryFiltersFields.TITLE
    ARTIST_NAME = QueryFiltersFields.ARTIST_NAME
    ALBUM_NAME = QueryFiltersFields.ALBUM_NAME
    GENRE_NAME = QueryFiltersFields.GENRE_NAME
    TAG_NAME = QueryFiltersFields.TAG_NAME
    PLAYLIST_NAME = QueryFiltersFields.PLAYLIST_NAME


def is_string1_part_of_string2_regardless_of_case(string1: str, string2: str) -> bool:
    return string1.lower() in string2.lower()


def lib_track_filter(queryset, request, *args, **kwargs):
    queryset = queryset.filter(user=request.user.id)
    if QueryFieldTypeValues.TITLE in request.query_params:
        request.query_params[QueryFieldTypeValues.TITLE]
        # TODO: handle type of query
    if QueryFields.QUERY in request.query_params:
        query = request.query_params[QueryFields.QUERY]
        if query != "":
            queryset = queryset.filter(title__icontains=query)
    return queryset.order_by(LibTrackFields.TITLE)


def manual_playlist_filter(queryset, request, *args, **kwargs):
    if QueryFields.QUERY in request.query_params:
        query = request.query_params[QueryFields.QUERY]
        if query != "":
            queryset = queryset.filter(
                name__icontains=query
            ).order_by(PlaylistFields.NAME)
    return queryset


def criteria_playlist_filter(queryset, request, *args, **kwargs):
    if QueryFields.QUERY in request.query_params:
        query = request.query_params[QueryFields.QUERY]
        unfiltered_queryset = queryset
        if query != "":
            queryset = unfiltered_queryset.filter(criteria__name__icontains=query)
            if is_string1_part_of_string2_regardless_of_case(query, CriterialessPlaylistNames.GENRE):
                queryset = queryset | unfiltered_queryset.filter(
                    criteria__isnull=True,
                    type_pk=CriteriaTypePks.GENRE)
            if is_string1_part_of_string2_regardless_of_case(query, CriterialessPlaylistNames.TAG):
                queryset = queryset | unfiltered_queryset.filter(
                    criteria__isnull=True,
                    type_pk=CriteriaTypePks.TAG)
    return queryset


def album_filter(queryset, request, *args, **kwargs):
    if QueryFields.QUERY in request.query_params:
        query = request.query_params[QueryFields.QUERY]
        if query != "":
            queryset = queryset.filter(name__icontains=query).order_by(AlbumFields.NAME)
    return queryset


def artist_filter(queryset, request, *args, **kwargs):
    if QueryFields.QUERY in request.query_params:
        query = request.query_params[QueryFields.QUERY]
        if query != "":
            queryset = queryset.filter(name__icontains=query).order_by(ArtistFields.NAME)
    return queryset


class SearchViewSet(ObjectMultipleModelAPIViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultMultipleModelLimitOffsetPagination

    # Only used by drf spectacular to generate the schema
    def get_detailed_serializer_class(self):
        return LibTrackDetailedSerializer

    @extend_schema(description=("""
                                Search within tracks, albums, artists and playlists.
                                The results is a set of four sets:
                                    - Playlist (searched and ordered by name);
                                    - Artist (searched and ordered by name);
                                    - Album (searched and ordered by name);
                                    - LibraryTrack (searched and ordered by title).
                                """))
    def get_querylist(self):
        user = self.request.user
        querylist = (
            {
                'queryset': LibraryTrack.objects.filter(user=user),
                'serializer_class': LibTrackDetailedSerializer,
                'filter_fn': lib_track_filter},
            {
                'queryset': ManualPlaylist.objects.filter(user=user),
                'serializer_class': ManualPlaylistSimpleSerializer,
                'filter_fn': manual_playlist_filter},
            {
                'queryset': CriteriaPlaylist.objects.filter(user=user),
                'serializer_class': CriteriaSimpleSerializer,
                'filter_fn': criteria_playlist_filter},
            {
                'queryset': Album.objects.filter(user=user),
                'serializer_class': AlbumMinimumSerializer,
                'filter_fn': album_filter},
            {
                'queryset': Artist.objects.filter(user=user),
                'serializer_class': ArtistSimpleSerializer,
                'filter_fn': artist_filter
            })

        return querylist
