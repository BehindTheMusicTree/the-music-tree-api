#!/usr/bin/env python

from django.http import JsonResponse
from rest_framework.response import Response

from django.db import IntegrityError

from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from bodzify_api.view import utility
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.serializer.criteria.CriteriaSerializer import (
    CriteriaRequestSerializer, CriteriaResponseSerializer)
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaType, CriteriaTypesLabels
from bodzify_api.model.playlist.criteria.TagPlaylist import TagPlaylist
from bodzify_api.model.playlist.criteria.GenrePlaylist import GenrePlaylist

NAME_FIELD = "name"
PARENT_FIELD = "parent"

class CriteriaViewSet(MultiSerializerViewSet):
  queryset = Criteria.objects.all()
  serializers = {
    'default': CriteriaRequestSerializer,
    'list':  CriteriaResponseSerializer,
    'retrieve':  CriteriaResponseSerializer,
  }

  def __init__(self, criteriaTypeLabel, **kwargs):
      if criteriaTypeLabel is None: 
        self.criteriaType = None
      else: 
        self.criteriaType = CriteriaType.objects.get(label=criteriaTypeLabel)
      super().__init__(**kwargs)

  def get_queryset(self):
    queryset = Criteria.objects.filter(user=self.request.user)
    
    name = self.request.query_params.get(NAME_FIELD)
    if name is not None: queryset = queryset.filter(name__contains=name)

    parentParameter = self.request.query_params.get(PARENT_FIELD)
    if parentParameter is not None:
      if parentParameter == "": parent = None
      else: parent = parentParameter
      queryset = queryset.filter(parent=parent)
      
    if self.criteriaType is not None:
      queryset = queryset.filter(type=self.criteriaType.id)

    return queryset
    
  @extend_schema(
    request=CriteriaRequestSerializer,
    responses=CriteriaResponseSerializer
  )
  def create(self, request, *args, **kwargs):
    requestSerializer = CriteriaRequestSerializer(data=request.data)
    requestSerializer.is_valid(raise_exception=True)
    try:
      criteria = requestSerializer.save(user=self.request.user, type=self.criteriaType)
    except IntegrityError as e:
      return utility.GetJsonResponseWhenBadRequest(exception=e)

    if self.criteriaType.label == CriteriaTypesLabels.GENRE:
      GenrePlaylist(user=self.request.user, criteria=criteria).save()
    elif self.criteriaType.label == CriteriaTypesLabels.TAG:
      TagPlaylist(user=self.request.user, criteria=criteria).save()

    responseSerializer = CriteriaResponseSerializer(criteria)
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
    responses=CriteriaResponseSerializer
  )
  def list(self, request, *args, **kwargs):
      queryset = self.filter_queryset(self.get_queryset())

      page = self.paginate_queryset(queryset)
      if page is not None:
          serializer = self.get_serializer(page, many=True)
          return self.get_paginated_response(serializer.data)

      serializer = self.get_serializer(queryset, many=True)
      return Response(serializer.data)