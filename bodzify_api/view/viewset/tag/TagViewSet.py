#!/usr/bin/env python

from django.http import JsonResponse
from rest_framework.response import Response

from django.db import IntegrityError

from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from bodzify_api.view import utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.serializer.tag.TagSerializer import TagRequestSerializer, TagResponseSerializer
from bodzify_api.model.tag.Tag import Tag
from bodzify_api.model.tag.TagType import TagType, TagTypesLabels

NAME_FIELD = "name"
PARENT_FIELD = "parent"

class TagViewSet(MultiSerializerViewSet):
  queryset = Tag.objects.all()
  serializers = {
    'default': TagRequestSerializer,
    'list':  TagResponseSerializer,
    'retrieve':  TagResponseSerializer,
  }

  def __init__(self, tagTypeLabel=TagTypesLabels.TAG, **kwargs):
      if tagTypeLabel is None: 
        self.tagType = None
      else: 
        self.tagType = TagType.objects.get(label=tagTypeLabel)
      super().__init__(**kwargs)

  def get_queryset(self):
    queryset = Tag.objects.filter(user=self.request.user)
    
    name = self.request.query_params.get(NAME_FIELD)
    if name is not None: queryset = queryset.filter(name__contains=name)

    parentParameter = self.request.query_params.get(PARENT_FIELD)
    if parentParameter is not None:
      if parentParameter == "": parent = None
      else: parent = parentParameter
      queryset = queryset.filter(parent=parent)
      
    if self.tagType is not None:
      queryset = queryset.filter(type=self.tagType.id)

    return queryset
    
  @extend_schema(
    request=TagRequestSerializer,
    responses=TagResponseSerializer
  )
  def create(self, request, *args, **kwargs):
    requestSerializer = TagRequestSerializer(data=request.data)
    requestSerializer.is_valid(raise_exception=True)
    try:
      if self.tagType is None:
        tag = requestSerializer.save(user=self.request.user)
      else:
        tag = requestSerializer.save(user=self.request.user, type=self.tagType)
    except IntegrityError as e:
      return utility.GetJsonResponseWhenBadRequest(exception=e)

    responseSerializer = TagResponseSerializer(tag)
    headers = self.get_success_headers(responseSerializer.data)
    
    return JsonResponse(
      responseSerializer.data, 
      status=status.HTTP_201_CREATED, 
      headers=headers,
      safe=False
    )

  @extend_schema(
    parameters=[
      OpenApiParameter(NAME_FIELD, OpenApiTypes.STR, OpenApiParameter.PATH),
      OpenApiParameter(PARENT_FIELD, OpenApiTypes.STR, OpenApiParameter.PATH)
    ],
    responses=TagResponseSerializer
  )
  def list(self, request, *args, **kwargs):
      queryset = self.filter_queryset(self.get_queryset())

      page = self.paginate_queryset(queryset)
      if page is not None:
          serializer = self.get_serializer(page, many=True)
          return self.get_paginated_response(serializer.data)

      serializer = self.get_serializer(queryset, many=True)
      return Response(serializer.data)