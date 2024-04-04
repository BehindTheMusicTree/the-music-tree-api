#!/usr/bin/env python

from django.db import transaction

from bodzify_api.model.Artist import Artist
from bodzify_api.serializer.artist.ArtistDetailedSerializer import ArtistDetailedSerializer
from bodzify_api.service.ArtistService import ArtistService
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class ArtistViewSet(AppModelViewSet):

    queryset = Artist.objects.all()
    serializers = {
        'default': ArtistDetailedSerializer,
        'list':  ArtistDetailedSerializer,
        'retrieve':  ArtistDetailedSerializer,
        'update':  ArtistDetailedSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(ArtistService(), **kwargs)

    def get_queryset(self):
        return Artist.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return self._destroy(request, *args, **kwargs)
