#!/usr/bin/env python

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from bodzify_api.serializer.playlist.PlaylistSerializer import PlaylistSerializer
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeLabels, PlaylistType

NAME_PARAMETER = "name"

class PlaylistViewSet(MultiSerializerViewSet):  
    queryset = Playlist.objects.all()
    serializers = {
        'default': PlaylistSerializer,
        'list':  PlaylistSerializer,
        'retrieve':  PlaylistSerializer,
    }

    def __init__(self, playlistTypeLabel=PlaylistTypeLabels.CUSTOM, **kwargs):
        if playlistTypeLabel is None: 
            self.playlistTypes = None
        else:
            self.playlistType = PlaylistType.objects.get(label=playlistTypeLabel)
        super().__init__(**kwargs)

    def get_queryset(self):
        queryset = Playlist.objects.filter(user=self.request.user)

        if self.playlistType is not None: queryset = queryset.filter(type=self.playlistType.id)
        
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