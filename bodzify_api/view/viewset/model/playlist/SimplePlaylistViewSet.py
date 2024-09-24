#!/usr/bin/env python

from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist, AttributesLabel
from bodzify_api.serializer.playlist.children.simple.input.endpoint \
    import SimplePlaylistInputEndpointSerializer
from bodzify_api.serializer.playlist.children.simple.output.with_tracks \
    import SimplePlaylistWithTracksSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.service.playlist.SimplePlaylistService import SimplePlaylistService


class GetFilterFields:
    NAME = AttributesLabel.NAME


class SimplePlaylistViewSet(AppModelViewSet):
    queryset = SimplePlaylist.objects.all()
    serializers = {
        "default": SimplePlaylistWithTracksSerializer,
        "list": SimplePlaylistWithTracksSerializer,
        "retrieve": SimplePlaylistWithTracksSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(SimplePlaylistService(), **kwargs)

    def get_queryset(self):
        queryset = SimplePlaylist.objects.filter(base_playlist__user=self.request.user)
        name_filter = self.request.GET.get(GetFilterFields.NAME)

        if name_filter is not None:
            queryset = queryset.filter(name__icontains=name_filter)
        return queryset.order_by(AttributesLabel.NAME)

    def _get_detailed_serializer(self, instance):
        return SimplePlaylistWithTracksSerializer(instance=instance)

    @extend_schema(parameters=[OpenApiParameter(name=GetFilterFields.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @transaction.atomic
    @extend_schema(request=SimplePlaylistInputEndpointSerializer, responses=SimplePlaylistWithTracksSerializer)
    def create(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @transaction.atomic
    @extend_schema(request=SimplePlaylistInputEndpointSerializer, responses=SimplePlaylistWithTracksSerializer)
    def update(self, request, *args, **kwargs):
        return self._update(request, *args, **kwargs)
