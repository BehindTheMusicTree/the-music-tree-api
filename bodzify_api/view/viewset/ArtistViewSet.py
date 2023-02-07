#!/usr/bin/env python

from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet


from bodzify_api.model.Artist import Artist
from bodzify_api.serializer.ArtistSerializer import ArtistSerializer

class ArtistViewSet(MultiSerializerViewSet):

    queryset = Artist.objects.all()
    serializers = {
        'default': ArtistSerializer,
        'list':  ArtistSerializer,
        'retrieve':  ArtistSerializer,
        'update':  ArtistSerializer,
    }

    def get_queryset(self):
        return Artist.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
         return super().destroy(request, *args, **kwargs)
