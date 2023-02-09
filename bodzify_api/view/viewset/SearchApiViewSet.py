#!/usr/bin/env python

from django.db.models import Q

from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
    
from bodzify_api.view.pagination.DefaultMultipleModelLimitOffsetPagination import (
    DefaultMultipleModelLimitOffsetPagination)

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.LibraryTrack import LibraryTrack

from bodzify_api.serializer.playlist.PlaylistWithoutTracksSerializer import (
    PlaylistWithoutTracksSerializer)
from bodzify_api.serializer.track.TrackDetailedSerializer import (
    TrackDetailedSerializer)

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
    type = request.query_params[TYPE_PARAMETER_TITLE_VALUE]
    query = request.query_params[QUERY_PARAMETER_NAME]
    if query != "":
        queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(artist__icontains=query) | 
                Q(album__icontains=query)
        )
    print(request.user)
    return queryset.filter(user=request.user.id)


def playlistFilter(queryset, request, *args, **kwargs):
    query = request.query_params[QUERY_PARAMETER_NAME]
    if query != "":
        queryset = queryset.filter(name__icontains=query)
    return queryset.filter(user=request.user.id)


class SearchApiViewSet(ObjectMultipleModelAPIViewSet):

    pagination_class = DefaultMultipleModelLimitOffsetPagination
    
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
        )

        return querylist
