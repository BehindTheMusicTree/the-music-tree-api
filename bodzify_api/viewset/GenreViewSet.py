#!/usr/bin/env python

from rest_framework import viewsets, exceptions
from rest_framework.pagination import PageNumberPagination

import logging

import django.views.defaults
from django.http import JsonResponse
from django.core.paginator import Paginator

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes

import bodzify_api.api.settings as apiSettings
from bodzify_api.serializers import GenreSerializer
from bodzify_api.dao.GenreDAO import GenreDAO
from bodzify_api.models import Genre
from django.contrib.auth.models import User

def getHttpResponseWhenPermissionDenied(request):
    return django.views.defaults.permission_denied(
                request=request, 
                exception=exceptions.PermissionDenied)

def getHttpResponseWhenIssueWithBadRequest(request):
    return django.views.defaults.bad_request(
                request=request, 
                exception=exceptions.bad_request)

def get_json_response_paginated(request, dataJsonList):
    pageNumber = request.GET.get(apiSettings.FIELD_PAGE, 0)
    paginator = Paginator(dataJsonList, PageNumberPagination.page_size)
    page_object = paginator.get_page(pageNumber)

    return JsonResponse({
        "count": len(dataJsonList),
        "current": pageNumber,
        "next": page_object.has_next(),
        "previous": page_object.has_previous(),
        "data": dataJsonList
    })

class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()