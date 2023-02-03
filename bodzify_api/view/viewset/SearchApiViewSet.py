#!/usr/bin/env python

from django.db.models import Q

from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
    
from bodzify_api.view.pagination.DefaultMultipleModelLimitOffsetPagination import (
    DefaultMultipleModelLimitOffsetPagination)

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.LibraryTrack import LibraryTrack

from bodzify_api.serializer.playlist.PlaylistWithoutTracksSerializer import (
    PlaylistWithoutTracksSerializer)
from bodzify_api.serializer.track.LibraryTrackResponseSerializer import (
    LibraryTrackResponseSerializer)

QUERY_FIELD_NAME = "query"


def libraryTrackFilter(queryset, request, *args, **kwargs):
    query = request.query_params[QUERY_FIELD_NAME]
    if query != "":
        queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(artist__icontains=query) | 
                Q(album__icontains=query)
        )
    print(request.user)
    return queryset.filter(user=request.user.id)


def playlistFilter(queryset, request, *args, **kwargs):
    query = request.query_params[QUERY_FIELD_NAME]
    if query != "":
        queryset = queryset.filter(name__icontains=query)
    return queryset.filter(user=request.user.id)


class SearchApiViewSet(ObjectMultipleModelAPIViewSet):

    pagination_class = DefaultMultipleModelLimitOffsetPagination
    
    def get_querylist(self):
        querylist = (
            {
                'queryset': LibraryTrack.objects.all(),
                'serializer_class': LibraryTrackResponseSerializer,
                'filter_fn': libraryTrackFilter
            },
            {
                'queryset': Playlist.objects.all(), 
                'serializer_class': PlaylistWithoutTracksSerializer,
                'filter_fn': playlistFilter
            },
        )

        return querylist
