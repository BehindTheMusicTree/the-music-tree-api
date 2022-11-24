#!/usr/bin/env python

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from bodzify_api.serializer.playlist.PlaylistSerializer import PlaylistSerializer
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.model.playlist.Playlist import Playlist

NAME_PARAMETER = "name"

class PlaylistViewSet(MultiSerializerViewSet):  
    queryset = Playlist.objects.all()
    serializers = {
        'default': PlaylistSerializer,
        'list':  PlaylistSerializer,
        'retrieve':  PlaylistSerializer,
    }

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