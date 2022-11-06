#!/usr/bin/env python

from rest_framework import viewsets, exceptions
from rest_framework.pagination import PageNumberPagination

import django.views.defaults
from django.http import JsonResponse
from django.core.paginator import Paginator

import bodzify_api.api.settings as apiSettings

RESPONSE_PAGINATED_COUNT = "count"
RESPONSE_PAGINATED_CURRENT = "current"
RESPONSE_PAGINATED_NEXT = "next"
RESPONSE_PAGINATED_PREVIOUS = "previous"
RESPONSE_PAGINATED_DATA = "data"

class BaseViewSet(viewsets.ModelViewSet):

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
            RESPONSE_PAGINATED_COUNT: len(dataJsonList),
            RESPONSE_PAGINATED_CURRENT: pageNumber,
            RESPONSE_PAGINATED_NEXT: page_object.has_next(),
            RESPONSE_PAGINATED_PREVIOUS: page_object.has_previous(),
            RESPONSE_PAGINATED_DATA: dataJsonList
        })