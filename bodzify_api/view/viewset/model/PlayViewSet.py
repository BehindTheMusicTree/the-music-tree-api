#!/usr/bin/env python

from django.db import transaction
from drf_spectacular.utils import extend_schema

from bodzify_api.model.Play import Fields, Play
from bodzify_api.serializer.schema.play.input.schema.endpoint.post import PlayPostSerializer
from bodzify_api.serializer.schema.play.output.detailed import PlayDetailedSerializer
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
        return Play.objects.filter(
            user=self.request.user).order_by(
            f"-{Fields.TIME} ")

    def _get_detailed_serializer(self, instance):
        return PlayDetailedSerializer(instance=instance)

    @transaction.atomic
    @extend_schema(request=PlayPostSerializer, responses=PlayDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)
