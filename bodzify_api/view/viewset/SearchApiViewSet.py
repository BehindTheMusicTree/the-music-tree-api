#!/usr/bin/env python

from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_spectacular.utils import extend_schema
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist \
    import CriteriaPlaylist, SPECIAL_NAMES as CRITERIA_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.criteria.output.without_tracks import CriteriaPlaylistWithoutTracksSerializer
from bodzify_api.serializer.playlist.children.simple.output.without_tracks import SimplePlaylistWithoutTracksSerializer
from bodzify_api.view.pagination.DefaultMultipleModelLimitOffsetPagination import \
    DefaultMultipleModelLimitOffsetPagination
from bodzify_api.model.Album import Album, ATTRIBUTES_LABEL as ATTRIBUTES_LABEL
from bodzify_api.model.Artist import Artist, ATTRIBUTES_LABEL as ARTIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.BasePlaylist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL as LIB_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.album.without_track import AlbumWithoutTracksSerializer
from bodzify_api.serializer.artist.detailed import ArtistDetailedSerializer
from bodzify_api.serializer.track.output.detailed import LibTrackDetailedSerializer
from rest_framework.permissions import IsAuthenticated


class QUERY_PARAMS_NAME:
    QUERY = "query"
    TYPE = "type"


class QUERY_FILTERS_FIELDS:
    TITLE = "title"
    ARTIST_NAME = "artist_name"
    ALBUM_NAME = "album_name"
    YEAR = "year"
    GENRE_NAME = "genre_name"
    TAG_NAME = "tag_name"
    PLAYLIST_NAME = "playlist_name"


class QUERY_PARAM_TYPE_VALUES:
    TITLE = QUERY_FILTERS_FIELDS.TITLE
    ARTIST_NAME = QUERY_FILTERS_FIELDS.ARTIST_NAME
    ALBUM_NAME = QUERY_FILTERS_FIELDS.ALBUM_NAME
    GENRE_NAME = QUERY_FILTERS_FIELDS.GENRE_NAME
    TAG_NAME = QUERY_FILTERS_FIELDS.TAG_NAME
    PLAYLIST_NAME = QUERY_FILTERS_FIELDS.PLAYLIST_NAME


def is_string1_part_of_string2_regardless_of_case(string1: str, string2: str) -> bool:
    return string1.lower() in string2.lower()


def lib_track_filter(queryset, request, *args, **kwargs):
    queryset = queryset.filter(user=request.user.id)
    if QUERY_PARAM_TYPE_VALUES.TITLE in request.query_params:
        request.query_params[QUERY_PARAM_TYPE_VALUES.TITLE]
        # TODO: handle type of query
    if QUERY_PARAMS_NAME.QUERY in request.query_params:
        query = request.query_params[QUERY_PARAMS_NAME.QUERY]
        if query != "":
            queryset = queryset.filter(title__icontains=query)
    return queryset.order_by(LIB_TRACK_ATTRIBUTES_LABEL.TITLE)


def simple_playlist_filter(queryset, request, *args, **kwargs):
    if QUERY_PARAMS_NAME.QUERY in request.query_params:
        query = request.query_params[QUERY_PARAMS_NAME.QUERY]
        if query != "":
            queryset = queryset.filter(
                name__icontains=query
            ).order_by(PLAYLIST_ATTRIBUTES_LABEL.NAME)
    return queryset


def criteria_playlist_filter(queryset, request, *args, **kwargs):
    if QUERY_PARAMS_NAME.QUERY in request.query_params:
        query = request.query_params[QUERY_PARAMS_NAME.QUERY]
        unfiltered_queryset = queryset
        if query != "":
            queryset = unfiltered_queryset.filter(criteria__name__icontains=query)
            if is_string1_part_of_string2_regardless_of_case(query, CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS):
                queryset = queryset | unfiltered_queryset.filter(
                    criteria__isnull=True,
                    type_id=CRITERIA_TYPES_ID.GENRE)
            if is_string1_part_of_string2_regardless_of_case(query, CRITERIA_PLAYLIST_SPECIAL_NAMES.TAGLESS):
                queryset = queryset | unfiltered_queryset.filter(
                    criteria__isnull=True,
                    type_id=CRITERIA_TYPES_ID.TAG)
    return queryset


def album_filter(queryset, request, *args, **kwargs):
    if QUERY_PARAMS_NAME.QUERY in request.query_params:
        query = request.query_params[QUERY_PARAMS_NAME.QUERY]
        if query != "":
            queryset = queryset.filter(name__icontains=query).order_by(ATTRIBUTES_LABEL.NAME)
    return queryset


def artist_filter(queryset, request, *args, **kwargs):
    if QUERY_PARAMS_NAME.QUERY in request.query_params:
        query = request.query_params[QUERY_PARAMS_NAME.QUERY]
        if query != "":
            queryset = queryset.filter(name__icontains=query).order_by(ARTIST_ATTRIBUTES_LABEL.NAME)
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
