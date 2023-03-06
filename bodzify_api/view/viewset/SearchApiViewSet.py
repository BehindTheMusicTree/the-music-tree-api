#!/usr/bin/env python
from django.db.models import F
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_spectacular.utils import extend_schema
from bodzify_api.view.pagination.DefaultMultipleModelLimitOffsetPagination import (
    DefaultMultipleModelLimitOffsetPagination)
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.album.AlbumWithoutTracksSerializer import AlbumWithoutTracksSerializer
from bodzify_api.serializer.artist.ArtistDetailedSerializer import ArtistDetailedSerializer
from bodzify_api.serializer.playlist.PlaylistWithoutTracksSerializer import (
    PlaylistWithoutTracksSerializer)
from bodzify_api.serializer.track.output.TrackDetailedSerializer import TrackDetailedSerializer

QUERY_PARAMETER_NAME = "query"
QUERY_TITLE_FILTER_NAME = "title"
QUERY_ARTIST_FILTER_NAME = "artist"
QUERY_ALBUM_FILTER_NAME = "album"
QUERY_YEAR_FILTER_NAME = "year"
QUERY_GENRE_FILTER_NAME = "genre"
QUERY_TAG_FILTER_NAME = "tag"
QUERY_PLAYLIST_FILTER_NAME = "playlist"

TYPE_PARAMETER_NAME = "type"
TYPE_PARAMETER_TITLE_VALUE = QUERY_TITLE_FILTER_NAME
TYPE_PARAMETER_ARTIST_VALUE = QUERY_ARTIST_FILTER_NAME
TYPE_PARAMETER_ALBUM_VALUE = QUERY_ALBUM_FILTER_NAME
TYPE_PARAMETER_GENRE_VALUE = QUERY_GENRE_FILTER_NAME
TYPE_PARAMETER_TAG_VALUE = QUERY_TAG_FILTER_NAME
TYPE_PARAMETER_PLAYLIST_VALUE = QUERY_PLAYLIST_FILTER_NAME


def libraryTrackFilter(queryset, request, *args, **kwargs):
    if TYPE_PARAMETER_TITLE_VALUE in request.query_params:
        type = request.query_params[TYPE_PARAMETER_TITLE_VALUE]
        # TODO: handle type of query
    if QUERY_PARAMETER_NAME in request.query_params:
        query = request.query_params[QUERY_PARAMETER_NAME]
        if query != "":
            queryset = queryset.filter(
                title__icontains=query
            ).order_by(LibraryTrack.ATTRIBUTE_TITLE_LABEL)
    return queryset.filter(user=request.user.id)


def playlistFilter(queryset, request, *args, **kwargs):
    query = request.query_params[QUERY_PARAMETER_NAME]
    if query != "":
        queryset = queryset.annotate(
            criteriaName=F(Playlist.ATTRIBUTE_CRITERIA_NAME_LABEL)
        ).filter(
            criteriaName__icontains=query
        ).order_by(Playlist.ATTRIBUTE_CRITERIA_NAME_LABEL)
    return queryset.filter(user=request.user.id)


def albumFilter(queryset, request, *args, **kwargs):
    query = request.query_params[QUERY_PARAMETER_NAME]
    if query != "":
        queryset = queryset.filter(name__icontains=query).order_by(
                Album.ATTRIBUTE_NAME_LABEL)
    return queryset.filter(user=request.user.id)


def artistFilter(queryset, request, *args, **kwargs):
    query = request.query_params[QUERY_PARAMETER_NAME]
    if query != "":
        queryset = queryset.filter(name__icontains=query).order_by(
                Artist.ATTRIBUTE_NAME_LABEL)
    return queryset.filter(user=request.user.id)


class SearchApiViewSet(ObjectMultipleModelAPIViewSet):

    pagination_class = DefaultMultipleModelLimitOffsetPagination
    
    @extend_schema(
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
        querylist = (
            {
                'queryset': LibraryTrack.objects.all(),
                'serializer_class': TrackDetailedSerializer,
                'filter_fn': libraryTrackFilter
            },
            {
                'queryset': Playlist.objects.all(), 
                'serializer_class': PlaylistWithoutTracksSerializer,
                'filter_fn': playlistFilter
            },
            {
                'queryset': Album.objects.all(), 
                'serializer_class': AlbumWithoutTracksSerializer,
                'filter_fn': albumFilter
            },
            {
                'queryset': Artist.objects.all(), 
                'serializer_class': ArtistDetailedSerializer,
                'filter_fn': artistFilter
            },
        )

        return querylist
