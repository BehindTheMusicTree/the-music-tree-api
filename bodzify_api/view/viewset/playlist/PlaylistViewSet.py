#!/usr/bin/env python

from rest_framework import viewsets

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from django.http import JsonResponse

from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackResponseSerializer
from bodzify_api.serializer.PlaylistSerializer import PlaylistSerializer
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.dao import MineTrackMyfreemp3Dao
import bodzify_api.view.utility as viewset_utility
from bodzify_api.model.playlist.Playlist import Playlist

NAME_PARAMETER = "name"

class PlaylistViewSet(viewsets.GenericViewSet):  
    queryset = Playlist.objects.all()

    def get_queryset(self):
        queryset = Playlist.objects.filter(user=self.request.user)
        
        name = self.request.query_params.get(NAME_PARAMETER)
        if name is not None: queryset = queryset.filter(name__contains=name)

        return queryset

    @extend_schema(
        parameters=[
          OpenApiParameter(NAME_PARAMETER, OpenApiTypes.STR, OpenApiParameter.PATH)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)