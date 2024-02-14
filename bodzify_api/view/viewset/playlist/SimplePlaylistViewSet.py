#!/usr/bin/env python
from django.http import JsonResponse
from rest_framework import status
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithTrackSerializer import \
    CriteriaPlaylistWithTracksSerializer
from bodzify_api.serializer.playlist.output.PlaylistWithoutParentSerializer import \
    PlaylistWithoutParentSerializer
from bodzify_api.service.PlaylistService import PlaylistService
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


class SimplePlaylistViewSet(MultiSerializerViewSet):
    queryset = SimplePlaylist.objects.all()
    serializers = {
        'default': PlaylistWithoutParentSerializer,
        'list':  PlaylistWithoutParentSerializer,
        'retrieve':  PlaylistWithoutParentSerializer,
    }
    
    def get_queryset(self):
        return SimplePlaylist.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        playlistService = PlaylistService()
        playlist = playlistService.create_simple_playlist(
            user=request.user, data=request.data)

        response_serializer = CriteriaPlaylistWithTracksSerializer(playlist)
        headers = self.get_success_headers(response_serializer.data)
        return JsonResponse(data=response_serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers,
                            safe=False)
