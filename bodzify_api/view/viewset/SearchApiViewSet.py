#!/usr/bin/env python
from django.db.models import F
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_spectacular.utils import extend_schema
from bodzify_api.view.pagination.DefaultMultipleModelLimitOffsetPagination import \
    DefaultMultipleModelLimitOffsetPagination
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.playlist.Playlist import Playlist, \
    ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack, \
    ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.album.AlbumWithoutTracksSerializer import AlbumWithoutTracksSerializer
from bodzify_api.serializer.artist.ArtistDetailedSerializer import ArtistDetailedSerializer
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithoutTracksSerializer import \
    CriteriaPlaylistWithoutTracksSerializer
from bodzify_api.serializer.track.output.TrackDetailedSerializer import TrackDetailedSerializer


class PARAMETER_NAME:
    QUERY = "query"
    TYPE = "type"


class QUERY_FILTERS_NAME:
    TITLE = "title"
    ARTIST_NAME = "artist_name"
    ALBUM_NAME = "album_name"
    YEAR = "year"
    GENRE_NAME = "genre_name"
    TAG_NAME = "tagName"
    PLAYLIST_NAME = "playlistName"


class TYPE_PARAMETER_VALUE:
    TITLE = QUERY_FILTERS_NAME.TITLE
    ARTIST_NAME = QUERY_FILTERS_NAME.ARTIST_NAME
    ALBUM_NAME = QUERY_FILTERS_NAME.ALBUM_NAME
    GENRE_NAME = QUERY_FILTERS_NAME.GENRE_NAME
    TAG_NAME = QUERY_FILTERS_NAME.TAG_NAME
    PLAYLIST_NAME = QUERY_FILTERS_NAME.PLAYLIST_NAME


def trackFilter(queryset, request, *args, **kwargs):
    if TYPE_PARAMETER_VALUE.TITLE in request.query_params:
        type = request.query_params[TYPE_PARAMETER_VALUE.TITLE]
        # TODO: handle type of query
    if PARAMETER_NAME.QUERY in request.query_params:
        query = request.query_params[PARAMETER_NAME.QUERY]
        if query != "":
            queryset = queryset.filter(
                title__icontains=query
            ).order_by(TRACK_ATTRIBUTES_LABEL.TITLE)
    return queryset.filter(user=request.user.id)


def playlistFilter(queryset, request, *args, **kwargs):
    query = request.query_params[PARAMETER_NAME.QUERY]
    if query != "":
        queryset = queryset.annotate(
            criteriaName=F(PLAYLIST_ATTRIBUTES_LABEL.CRITERIA_NAME)
        ).filter(
            criteriaName__icontains=query
        ).order_by(PLAYLIST_ATTRIBUTES_LABEL.CRITERIA_NAME)
    return queryset.filter(user=request.user.id)


def albumFilter(queryset, request, *args, **kwargs):
    query = request.query_params[PARAMETER_NAME.QUERY]
    if query != "":
        queryset = queryset.filter(name__icontains=query).order_by(
            Album.ATTRIBUTE_NAME_LABEL)
    return queryset.filter(user=request.user.id)


def artistFilter(queryset, request, *args, **kwargs):
    query = request.query_params[PARAMETER_NAME.QUERY]
    if query != "":
        queryset = queryset.filter(name__icontains=query).order_by(
            Artist.ATTRIBUTE_NAME_LABEL)
    return queryset.filter(user=request.user.id)


class SearchApiViewSet(ObjectMultipleModelAPIViewSet):

    pagination_class = DefaultMultipleModelLimitOffsetPagination

    @extend_schema(description=("""
                                Search within tracks, albums, artists and playlists.
                                The results is a set of four sets:
                                    - Playlist (searched and ordered by name);
                                    - Artist (searched and ordered by name);
                                    - Album (searched and ordered by name);
                                    - LibraryTrack (searched and ordered by title).
                                """))
    def get_querylist(self):
        querylist = (
            {
                'queryset': LibraryTrack.objects.all(),
                'serializer_class': TrackDetailedSerializer,
                'filter_fn': trackFilter},
            {
                'queryset': Playlist.objects.all(),
                'serializer_class': CriteriaPlaylistWithoutTracksSerializer,
                'filter_fn': playlistFilter},
            {
                'queryset': Album.objects.all(),
                'serializer_class': AlbumWithoutTracksSerializer,
                'filter_fn': albumFilter},
            {
                'queryset': Artist.objects.all(),
                'serializer_class': ArtistDetailedSerializer,
                'filter_fn': artistFilter
            })

        return querylist
