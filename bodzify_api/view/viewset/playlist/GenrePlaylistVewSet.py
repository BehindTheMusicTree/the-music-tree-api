#!/usr/bin/env python

from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from django.http import JsonResponse

from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackResponseSerializer
from bodzify_api.serializer.PlaylistSerializer import PlaylistSerializer
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.dao import MineTrackMyfreemp3Dao
import bodzify_api.view.utility as viewset_utility
from bodzify_api.model.playlist.GenrePlaylist import TagPlaylist
from bodzify_api.view.viewset.playlist.PlaylistViewSet import PlaylistViewSet

PARENT_PARAMETER = "parent"

class GenrePlaylistViewSet(PlaylistViewSet):  
    queryset = TagPlaylist.objects.all()
    serializers = {
        'default': PlaylistSerializer,
        'list':  PlaylistSerializer,
        'retrieve':  PlaylistSerializer,
    }

    def get_queryset(self):
        queryset = TagPlaylist.objects.all()
        
        parent = self.request.query_params.get(PARENT_PARAMETER)
        if parent is not None: queryset = queryset.filter(genre__parent__name=parent)

        return queryset