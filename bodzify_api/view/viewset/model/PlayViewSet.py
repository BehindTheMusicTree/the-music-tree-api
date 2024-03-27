#!/usr/bin/env python

from drf_spectacular.utils import extend_schema

from bodzify_api.model.play.Play import Play
from bodzify_api.serializer.play.input.schema.endpoint.PlayPostSchemaSerializer import PlayPostSerializer
from bodzify_api.serializer.play.output.PlayDetailedSerializer import PlayDetailedSerializer
from bodzify_api.service.PlayService import PlayService
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class PlayViewSet(AppModelViewSet):
    queryset = Play.objects.all()
    serializers = {
        "default": PlayDetailedSerializer,
        "list": PlayDetailedSerializer,
        "retrieve": PlayDetailedSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(PlayService(), **kwargs)

    def get_queryset(self):
        return Play.objects.filter(playlist__user=self.request.user)

    def _get_detailed_serializer(self, instance):
        return PlayDetailedSerializer(instance=instance)

    @extend_schema(request=PlayPostSerializer, responses=PlayDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)
