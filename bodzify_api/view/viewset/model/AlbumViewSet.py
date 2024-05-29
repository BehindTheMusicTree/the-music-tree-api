#!/usr/bin/env python

from django.db import transaction

from bodzify_api.model.Album import ATTRIBUTES_LABEL, Album
from bodzify_api.serializer.album.output.detailed import AlbumDetailedSerializer
from bodzify_api.service.AlbumService import AlbumService
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class AlbumViewSet(AppModelViewSet):

    queryset = Album.objects.all()
    serializers = {
        'default': AlbumDetailedSerializer,
        'list':  AlbumDetailedSerializer,
        'retrieve':  AlbumDetailedSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(AlbumService(), **kwargs)

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user).order_by(ATTRIBUTES_LABEL.NAME)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return self._destroy(request, *args, **kwargs)
