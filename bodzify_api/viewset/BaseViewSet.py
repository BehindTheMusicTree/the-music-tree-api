#!/usr/bin/env python

import os

from rest_framework import viewsets, exceptions
from rest_framework.pagination import PageNumberPagination

import django.views.defaults
from django.http import JsonResponse, FileResponse
from django.core.paginator import Paginator

import bodzify_api.api.settings as apiSettings

RESPONSE_PAGINATED_COUNT_FIELD = "count"
RESPONSE_PAGINATED_CURRENT_FIELD = "current"
RESPONSE_PAGINATED_NEXT_FIELD = "next"
RESPONSE_PAGINATED_PREVIOUS_FIELD = "previous"
RESPONSE_PAGINATED_RESULTS_FIELD = "results"

RESPONSE_FILE_CONTENT_TYPE_VALUE ='file'
RESPONSE_FILE_CONTENT_LENGTH_FIELD ='Content-Length'
RESPONSE_FILE_CONTENT_DISPOSITION_FIELD ='Content-Disposition'
RESPONSE_FILE_CONTENT_DISPOSITION_FILE_VALUE ='attachment; filename="%s"'
RESPONSE_FILE_CONTENT_LENGTH_FIELD ='Content-Length'
RESPONSE_FILE_CONTENT_LENGTH_FIELD ='Content-Length'

class BaseViewSet(viewsets.ModelViewSet):

    def getHttpResponseWhenPermissionDenied(request):
        return django.views.defaults.permission_denied(
                    request=request, 
                    exception=exceptions.PermissionDenied)

    def getHttpResponseWhenIssueWithBadRequest(request):
        return django.views.defaults.bad_request(
                    request=request, 
                    exception=exceptions.bad_request)

    def getJsonResponsePaginated(request, dataJsonList):
        pageNumber = request.GET.get(apiSettings.FIELD_PAGE, 0)
        paginator = Paginator(dataJsonList, PageNumberPagination.page_size)
        page_object = paginator.get_page(pageNumber)

        return JsonResponse({
            RESPONSE_PAGINATED_COUNT_FIELD: len(dataJsonList),
            RESPONSE_PAGINATED_CURRENT_FIELD: pageNumber,
            RESPONSE_PAGINATED_NEXT_FIELD: page_object.has_next(),
            RESPONSE_PAGINATED_PREVIOUS_FIELD: page_object.has_previous(),
            RESPONSE_PAGINATED_RESULTS_FIELD: dataJsonList
        })

    def getFileResponseForTrackDownload(request, trackModel):
        fileHandle = open(trackModel.path, "rb")
        response = FileResponse(fileHandle, content_type=RESPONSE_FILE_CONTENT_TYPE_VALUE)
        response[RESPONSE_FILE_CONTENT_LENGTH_FIELD] = os.path.getsize(trackModel.path)
        response[RESPONSE_FILE_CONTENT_DISPOSITION_FIELD] = RESPONSE_FILE_CONTENT_DISPOSITION_FILE_VALUE % trackModel.filename
        return response