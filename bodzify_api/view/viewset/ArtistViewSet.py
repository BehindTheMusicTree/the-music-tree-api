#!/usr/bin/env python

from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.model.Artist import Artist
import bodzify_api.service.ArtistService as ArtistService
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
        user = request.user
        artist = self.get_object()
        if Artist.objects.filter(user=user, uuid=artist.uuid).exists() == False:
             raise APIException.NotFound(detail=None, code=None)
        
        ArtistService.DeleteArtistAndRelativeAlbumsAndTracks(user=user, artist=artist)
        return Response(status=status.HTTP_204_NO_CONTENT)
