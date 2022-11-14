#!/usr/bin/env python

from django.http import JsonResponse

from rest_framework import viewsets, status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.serializer.GenreSerializer import GenreRequestSerializer, GenreResponseSerializer
from bodzify_api.models import Genre

NAME_FIELD = "name"
PARENT_FIELD = "parent"

class GenreViewSet(MultiSerializerViewSet):
    queryset = Genre.objects.all()
    serializers = {
        'default': GenreRequestSerializer,
        'list':  GenreResponseSerializer,
        'retrieve':  GenreResponseSerializer,
    }

    def get_queryset(self):
        queryset = Genre.objects.all()
        name = self.request.query_params.get(NAME_FIELD)
        parentParameter = self.request.query_params.get(PARENT_FIELD)

        if parentParameter == "": parent = None
        else: parent = parentParameter

        if name is None: queryset = queryset.filter(parent=parent)
        else: queryset = queryset.filter(name__contains=name, parent=parent)
        
        return queryset

    @extend_schema(
      request=GenreRequestSerializer,
      responses=GenreResponseSerializer
    )
    def create(self, request, *args, **kwargs):
        requestSerializer = self.get_serializer(data=request.data)
        requestSerializer.is_valid(raise_exception=True)
        genre = requestSerializer.save(user=self.request.user)
        responseSerializer = GenreResponseSerializer(genre)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(responseSerializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
      parameters=[
        OpenApiParameter(NAME_FIELD, OpenApiTypes.STR, OpenApiParameter.PATH),
        OpenApiParameter(PARENT_FIELD, OpenApiTypes.STR, OpenApiParameter.PATH)
      ],
      responses=GenreResponseSerializer
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)