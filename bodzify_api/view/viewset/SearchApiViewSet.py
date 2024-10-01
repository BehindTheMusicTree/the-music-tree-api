#!/usr/bin/env python

from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_spectacular.utils import extend_schema
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.children.CriteriaPlaylist \
    import CriteriaPlaylist, SpecialNames as CRITERIA_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.criteria.output.without_tracks import CriteriaPlaylistWithoutTracksSerializer
from bodzify_api.serializer.playlist.children.simple.output.without_tracks import SimplePlaylistWithoutTracksSerializer
from bodzify_api.view.pagination.DefaultMultipleModelLimitOffsetPagination import \
    DefaultMultipleModelLimitOffsetPagination
from bodzify_api.model.Album import Album, AttributesLabel as AttributesLabel
from bodzify_api.model.Artist import Artist, AttributesLabel as ArtistAttributesLabels
from bodzify_api.model.playlist.BasePlaylist import AttributesLabel as PlaylistAttributesLabels
from bodzify_api.model.track.LibraryTrack import LibraryTrack, AttributesLabel as LibTrackAttributesLabels
from bodzify_api.serializer.album.without_track import AlbumWithoutTracksSerializer
from bodzify_api.serializer.artist.detailed import ArtistDetailedSerializer
from bodzify_api.serializer.track.output.detailed import LibTrackDetailedSerializer
from rest_framework.permissions import IsAuthenticated


class QueryFields:
    QUERY = "query"
    TYPE = 'type'


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
    return queryset.order_by(LibTrackAttributesLabels.TITLE)


def simple_playlist_filter(queryset, request, *args, **kwargs):
    if QueryFields.QUERY in request.query_params:
        query = request.query_params[QueryFields.QUERY]
        if query != "":
            queryset = queryset.filter(
                name__icontains=query
            ).order_by(PlaylistAttributesLabels.NAME)
    return queryset


def criteria_playlist_filter(queryset, request, *args, **kwargs):
    if QueryFields.QUERY in request.query_params:
        query = request.query_params[QueryFields.QUERY]
        unfiltered_queryset = queryset
        if query != "":
            queryset = unfiltered_queryset.filter(criteria__name__icontains=query)
            if is_string1_part_of_string2_regardless_of_case(query, CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS):
                queryset = queryset | unfiltered_queryset.filter(
                    criteria__isnull=True,
                    type_id=CriteriaTypesId.GENRE)
            if is_string1_part_of_string2_regardless_of_case(query, CRITERIA_PLAYLIST_SPECIAL_NAMES.TAGLESS):
                queryset = queryset | unfiltered_queryset.filter(
                    criteria__isnull=True,
                    type_id=CriteriaTypesId.TAG)
    return queryset


def album_filter(queryset, request, *args, **kwargs):
    if QueryFields.QUERY in request.query_params:
        query = request.query_params[QueryFields.QUERY]
        if query != "":
            queryset = queryset.filter(name__icontains=query).order_by(AttributesLabel.NAME)
    return queryset


def artist_filter(queryset, request, *args, **kwargs):
    if QueryFields.QUERY in request.query_params:
        query = request.query_params[QueryFields.QUERY]
        if query != "":
            queryset = queryset.filter(name__icontains=query).order_by(ArtistAttributesLabels.NAME)
    return queryset


class SearchApiViewSet(ObjectMultipleModelAPIViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultMultipleModelLimitOffsetPagination

    # Only used by drf spectacular to generate the schema
    def get_serializer_class(self):
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
                'queryset': SimplePlaylist.objects.filter(base_playlist__user=user),
                'serializer_class': SimplePlaylistWithoutTracksSerializer,
                'filter_fn': simple_playlist_filter},
            {
                'queryset': CriteriaPlaylist.objects.filter(base_playlist__user=user),
                'serializer_class': CriteriaPlaylistWithoutTracksSerializer,
                'filter_fn': criteria_playlist_filter},
            {
                'queryset': Album.objects.filter(user=user),
                'serializer_class': AlbumWithoutTracksSerializer,
                'filter_fn': album_filter},
            {
                'queryset': Artist.objects.filter(user=user),
                'serializer_class': ArtistDetailedSerializer,
                'filter_fn': artist_filter
            })

        return querylist
