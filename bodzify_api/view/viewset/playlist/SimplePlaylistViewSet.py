#!/usr/bin/env python

from django.http import JsonResponse
from rest_framework import status
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.PlaylistWithTrackSerializer import \
    PlaylistWithTrackSerializer
from bodzify_api.service.PlaylistService import PlaylistService
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


class SimplePlaylistViewSet(MultiSerializerViewSet):
    queryset = SimplePlaylist.objects.all()
    serializers = {
        'default': PlaylistWithTrackSerializer,
        'list':  PlaylistWithTrackSerializer,
        'retrieve':  PlaylistWithTrackSerializer,
    }

    def create(self, request, *args, **kwargs):
        playlistService = PlaylistService()
        playlist = playlistService.createSimplePlaylist(user=request.user, data=request.data)

        responseSerializer = PlaylistWithTrackSerializer(playlist)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(data=responseSerializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers,
                            safe=False)
