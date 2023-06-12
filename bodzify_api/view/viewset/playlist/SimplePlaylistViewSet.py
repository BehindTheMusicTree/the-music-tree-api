#!/usr/bin/env python

from django.http import JsonResponse
from rest_framework import status
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.output.PlaylistWithTrackSerializer import \
    PlaylistWithTracksSerializer
from bodzify_api.service.PlaylistService import PlaylistService
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


class SimplePlaylistViewSet(MultiSerializerViewSet):
    queryset = SimplePlaylist.objects.all()
    serializers = {
        'default': PlaylistWithTracksSerializer,
        'list':  PlaylistWithTracksSerializer,
        'retrieve':  PlaylistWithTracksSerializer,
    }

    def create(self, request, *args, **kwargs):
        playlistService = PlaylistService()
        playlist = playlistService.CreateSimplePlaylist(user=request.user, data=request.data)

        responseSerializer = PlaylistWithTracksSerializer(playlist)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(data=responseSerializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers,
                            safe=False)
