#!/usr/bin/env python

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from bodzify_api.serializer.playlist.PlaylistSerializer import PlaylistSerializer
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds, PlaylistType

NAME_PARAMETER = "name"
PARENT_UUID_PARAMETER = "parent"
TYPE_LABEL_PARAMETER = "type"

class PlaylistViewSet(MultiSerializerViewSet):  
    queryset = Playlist.objects.all()
    serializers = {
        'default': PlaylistSerializer,
        'list':  PlaylistSerializer,
        'retrieve':  PlaylistSerializer,
    }

    def __init__(self, playlistTypeLabel=None, **kwargs):
        if playlistTypeLabel is None: 
            self.playlistType = None
        else:
            self.playlistType = PlaylistType.objects.get(label=playlistTypeLabel)
        super().__init__(**kwargs)

    def get_queryset(self):
        queryset = Playlist.objects.filter(user=self.request.user)

        if self.playlistType is not None: queryset = queryset.filter(type=self.playlistType.id)
        
        name = self.request.query_params.get(NAME_PARAMETER)
        if name is not None: queryset = queryset.filter(name__contains=name)

        parentUuidParameterValue = self.request.query_params.get(PARENT_UUID_PARAMETER)
        if parentUuidParameterValue is not None: 
            if parentUuidParameterValue == "": 
                parentUuidFilter = None
            else : 
                parentUuidFilter = parentUuidParameterValue
            queryset = queryset.filter(criteria__parent__uuid=parentUuidFilter)

        typeLabel = self.request.query_params.get(TYPE_LABEL_PARAMETER)
        if typeLabel is not None: queryset = queryset.filter(type__label=typeLabel)

        return queryset

    @extend_schema(
        parameters=[
          OpenApiParameter(NAME_PARAMETER, OpenApiTypes.STR, OpenApiParameter.PATH),
          OpenApiParameter(PARENT_UUID_PARAMETER, OpenApiTypes.STR, OpenApiParameter.PATH),
          OpenApiParameter(TYPE_LABEL_PARAMETER, OpenApiTypes.STR, OpenApiParameter.PATH)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)