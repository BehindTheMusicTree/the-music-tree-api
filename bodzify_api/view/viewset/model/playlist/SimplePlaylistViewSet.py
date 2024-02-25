#!/usr/bin/env python

from django.http import JsonResponse
from rest_framework import status
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from bodzify_api.model.Album import ATTRIBUTES_LABEL
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithTracksSerializer import \
    CriteriaPlaylistWithTracksSerializer
from bodzify_api.serializer.playlist.output.PlaylistSerializer import PlaylistSerializer
from bodzify_api.serializer.playlist.simple.input.schema.SimplePlaylistPostSchemaSerializer import SimplePlaylistPostSchemaSerializer
from bodzify_api.serializer.playlist.simple.output.SimplePlaylistWithTracksSerializer \
    import SimplePlaylistWithTracksSerializer
from bodzify_api.service.playlist.PlaylistService import PlaylistService
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.service.playlist.SimplePlaylistService import SimplePlaylistService


class GET_FILTER_FIELDS:
    NAME = ATTRIBUTES_LABEL.NAME


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
        queryset = SimplePlaylist.objects.filter(playlist__user=self.request.user)
        name_filter = self.request.GET.get(GET_FILTER_FIELDS.NAME)

        if name_filter is not None:
            queryset = queryset.filter(name__icontains=name_filter)
        return queryset

    def _get_detailed_serializer(self, instance):
        return SimplePlaylistWithTracksSerializer(instance=instance)

    @extend_schema(parameters=[
        OpenApiParameter(name=GET_FILTER_FIELDS.NAME,
                         type=OpenApiTypes.STR,
                         location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(request=SimplePlaylistPostSchemaSerializer,
                   responses=SimplePlaylistWithTracksSerializer)
    def create(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)
