#!/usr/bin/env python

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # type: ignore
from django.db import transaction

from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.service.TrackService import TrackService
from bodzify_api.serializer.schema.track.output.detailed import LibTrackDetailedSerializer
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.filter.LibTrackFilterSet import LibTrackFilterSet, Fields as FilterFields


class TrackViewSet(AppModelViewSet):
    def __init__(self, **kwargs):
        super().__init__(
            service=TrackService(),
            model_class=LibraryTrack,
            filter_class=LibTrackFilterSet,
            detailed_serializer_class=LibTrackDetailedSerializer,
            **kwargs
        )

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.TITLE, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ARTISTS_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ALBUM_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.GENRE_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.LANGUAGE, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return self._destroy(request, *args, **kwargs)
