#!/usr/bin/env python

from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from bodzify_api.filter.ArtistFilter import ArtistFilter, Fields as FilterFields
from bodzify_api.model.Artist import Artist, Fields as ModelFields
from bodzify_api.serializer.schema.artist.detailed import ArtistDetailedSerializer
from bodzify_api.serializer.schema.artist.minimum import ArtistMinimumSerializer
from bodzify_api.service.ArtistService import ArtistService
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class ArtistViewSet(AppModelViewSet):
    queryset = Artist.objects.all()
    serializers = {
        'default': ArtistDetailedSerializer,
        'list':  ArtistMinimumSerializer,
        'retrieve':  ArtistDetailedSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(ArtistService(), **kwargs)

    def get_queryset(self):
        try:
            snake_case_params = self.get_dict_in_snake_case_keys_from_dict_in_camel_case_keys(self.request.GET)
            queryset = Artist.objects.filter(user=self.request.user)
            filtered_queryset = ArtistFilter(snake_case_params, queryset=queryset).qs
            return filtered_queryset.order_by(f"-{ModelFields.CREATED_ON}")
        except ValidationError as e:
            raise ValidationError(e.detail)

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"detail": str(e.detail[0])},
                status=status.HTTP_400_BAD_REQUEST
            )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return self._destroy(request, *args, **kwargs)
