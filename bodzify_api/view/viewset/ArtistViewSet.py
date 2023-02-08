#!/usr/bin/env python

from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


from bodzify_api.model.Artist import Artist
from bodzify_api.serializer.artist.ArtistDetailedSerializer import ArtistDetailedSerializer

class ArtistViewSet(MultiSerializerViewSet):

    queryset = Artist.objects.all()
    serializers = {
        'default': ArtistDetailedSerializer,
        'list':  ArtistDetailedSerializer,
        'retrieve':  ArtistDetailedSerializer,
        'update':  ArtistDetailedSerializer,
    }

    def get_queryset(self):
        return Artist.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
         return super().destroy(request, *args, **kwargs)
