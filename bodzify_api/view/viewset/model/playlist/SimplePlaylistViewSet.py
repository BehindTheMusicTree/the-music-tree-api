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
from bodzify_api.serializer.playlist.simple.output.SimplePlaylistWithTracksSerializer import SimplePlaylistWithTracksSerializer
from bodzify_api.service.playlist.PlaylistService import PlaylistService
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet

class GET_FILTER_FIELDS:
    NAME = ATTRIBUTES_LABEL.NAME

class SimplePlaylistViewSet(AppModelViewSet):
    queryset = SimplePlaylist.objects.all()
    serializers = {
        "default": PlaylistSerializer,
        "list": PlaylistSerializer,
        "retrieve": PlaylistSerializer,
    }

    def __init__(self, service, **kwargs):
        super().__init__(SimplePlaylistService(), **kwargs)

    def get_queryset(self):
        return SimplePlaylist.objects.filter(playlist__user=self.request.user)

    def _get_detailed_serializer(self, instance):
        return SimplePlaylistWithTracksSerializer(instance=instance)


    OpenApiParameter(name=GET_FILTER_FIELDS.NAME,
                        type=OpenApiTypes.STR,
                        location=OpenApiParameter.QUERY))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        playlistService = PlaylistService()
        playlist = playlistService.create_simple_playlist(user=request.user, data=request.data)

        response_serializer = CriteriaPlaylistWithTracksSerializer(playlist)
        headers = self.get_success_headers(response_serializer.data)
        return JsonResponse(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
            safe=False,
        )
