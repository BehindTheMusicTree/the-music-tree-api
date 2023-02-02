#!/usr/bin/env python

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from bodzify_api.serializer.playlist.PlaylistWithTrackSerializer import (
    PlaylistWithTrackSerializer
)

from bodzify_api.view.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.model.playlist.Playlist import Playlist

NAME_PARAMETER = "name"
PARENT_UUID_PARAMETER = "parent"
TYPE_LABEL_PARAMETER = "type"


class PlaylistViewSet(MultiSerializerViewSet):
    queryset = Playlist.objects.all()
    serializers = {
        'default': PlaylistWithTrackSerializer,
        'list':  PlaylistWithTrackSerializer,
        'retrieve':  PlaylistWithTrackSerializer,
    }

    def get_queryset(self):
        queryset = Playlist.objects.filter(user=self.request.user)

        name = self.request.query_params.get(NAME_PARAMETER)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        parentUuidParameterValue = self.request.query_params.get(PARENT_UUID_PARAMETER)
        if parentUuidParameterValue is not None:
            if parentUuidParameterValue == "":
                parentUuidFilter = None
            else:
                parentUuidFilter = parentUuidParameterValue
            queryset = queryset.filter(criteria__parent__uuid=parentUuidFilter)

        typeLabel = self.request.query_params.get(TYPE_LABEL_PARAMETER)
        if typeLabel is not None:
            queryset = queryset.filter(type__label=typeLabel)

        return queryset

    @extend_schema(
        parameters=[
          OpenApiParameter(
            name=NAME_PARAMETER,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY),
          OpenApiParameter(
            name=PARENT_UUID_PARAMETER,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY),
          OpenApiParameter(
            name=TYPE_LABEL_PARAMETER,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
