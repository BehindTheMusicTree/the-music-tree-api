#!/usr/bin/env python

from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from bodzify_api.model.Album import Album, Fields as ModelFields
from bodzify_api.filter.AlbumFilter import AlbumFilter, Fields as FilterFields
from bodzify_api.serializer.schema.album.detailed import AlbumDetailedSerializer
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
        try:
            snake_case_params = self.get_dict_in_snake_case_keys_from_dict_in_camel_case_keys(self.request.GET)
            queryset = Album.objects.filter(user=self.request.user)
            filtered_queryset = AlbumFilter(snake_case_params, queryset=queryset).qs
            return filtered_queryset.order_by(f"-{ModelFields.CREATED_ON}")
        except ValidationError as e:
            raise ValidationError(e.detail)

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ALBUM_ARTISTS_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"detail": str(e.detail[0])},
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return self._destroy(request, *args, **kwargs)
