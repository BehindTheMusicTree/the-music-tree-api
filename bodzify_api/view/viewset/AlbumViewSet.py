#!/usr/bin/env python
from rest_framework import status
from rest_framework.response import Response
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.model.Album import Album
from bodzify_api.serializer.album.AlbumDetailedSerializer import AlbumDetailedSerializer

class AlbumViewSet(MultiSerializerViewSet):

    queryset = Album.objects.all()
    serializers = {
        'default': AlbumDetailedSerializer,
        'list':  AlbumDetailedSerializer,
        'retrieve':  AlbumDetailedSerializer,
    }

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        self.get_object().deleteWithTracksAndEventuallyArtists()
        return Response(status=status.HTTP_204_NO_CONTENT)
