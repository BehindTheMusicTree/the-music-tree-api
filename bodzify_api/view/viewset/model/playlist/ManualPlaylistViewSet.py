#!/usr/bin/env python

from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from bodzify_api.model.playlist.children.ManualPlaylist import Fields, ManualPlaylist
from bodzify_api.serializer.schema.playlist.children.simple.input.endpoint import ManualPlaylistInputEndpointSerializer
from bodzify_api.serializer.schema.playlist.children.simple.output.detailed import ManualPlaylistDetailedSerializer
from bodzify_api.service.playlist.ManualPlaylistService import ManualPlaylistService
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class GetFilterFields:
    NAME = Fields.NAME


class ManualPlaylistViewSet(AppModelViewSet):
    queryset = ManualPlaylist.objects.all()
    serializers = {
        "default": ManualPlaylistDetailedSerializer,
        "list": ManualPlaylistDetailedSerializer,
        "retrieve": ManualPlaylistDetailedSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(ManualPlaylistService(), **kwargs)

    def get_queryset(self):
        queryset = ManualPlaylist.objects.filter(user=self.request.user)
        name_filter = self.request.GET.get(GetFilterFields.NAME)

        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)
        return queryset.order_by(Fields.NAME)

    def _get_detailed_serializer(self, instance):
        return ManualPlaylistDetailedSerializer(instance=instance)

    @extend_schema(parameters=[OpenApiParameter(name=GetFilterFields.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @transaction.atomic
    @extend_schema(request=ManualPlaylistInputEndpointSerializer, responses=ManualPlaylistDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @transaction.atomic
    @extend_schema(request=ManualPlaylistInputEndpointSerializer, responses=ManualPlaylistDetailedSerializer)
    def update(self, request, *args, **kwargs):
        return self._update(request, *args, **kwargs)
