#!/usr/bin/env python

import os

from rest_framework import exceptions
from rest_framework.pagination import PageNumberPagination

from django.db import IntegrityError
import django.views.defaults
from django.http import JsonResponse, FileResponse
from django.core.paginator import Paginator


INTEGRITY_ERROR_MESSAGE = "There is an issue with the object sent"

RESPONSE_FILE_CONTENT_TYPE_VALUE ='file'
RESPONSE_FILE_CONTENT_LENGTH_FIELD ='Content-Length'
RESPONSE_FILE_CONTENT_DISPOSITION_FIELD ='Content-Disposition'
RESPONSE_FILE_CONTENT_DISPOSITION_FILE_VALUE ='attachment; filename="%s"'
RESPONSE_FILE_CONTENT_LENGTH_FIELD ='Content-Length'
RESPONSE_FILE_CONTENT_LENGTH_FIELD ='Content-Length'

PAGINATED_COUNT_FIELD = "count"
PAGINATED_CURRENT_FIELD = "current"
PAGINATED_NEXT_FIELD = "next"
PAGINATED_PREVIOUS_FIELD = "previous"
PAGINATED_RESULTS_FIELD = "results"

REQUEST_QUERY_FIELD = "query"
REQUEST_PAGINATED_PAGE_FIELD = "page"
REQUEST_PAGINATED_PAGE_SIZE_FIELD = "pageSize"


def GetHttpResponseWhenPermissionDenied(request):
    return django.views.defaults.permission_denied(
                request=request, 
                exception=exceptions.PermissionDenied)


def GetJsonResponseWhenBadRequest(exception = exceptions.bad_request):
    if type(exception) == IntegrityError:
        errorMessage = INTEGRITY_ERROR_MESSAGE
    else:
        errorMessage = str(exception)
    return JsonResponse({
                'success': False, 
                'errors': errorMessage
            })


def GetJsonResponsePaginated(request, dataJsonList):
    pageNumber = request.GET.get(REQUEST_PAGINATED_PAGE_FIELD, 0)
    paginator = Paginator(dataJsonList, PageNumberPagination.page_size)
    page_object = paginator.get_page(pageNumber)

    return JsonResponse({
        PAGINATED_COUNT_FIELD: len(dataJsonList),
        PAGINATED_CURRENT_FIELD: pageNumber,
        PAGINATED_NEXT_FIELD: page_object.has_next(),
        PAGINATED_PREVIOUS_FIELD: page_object.has_previous(),
        PAGINATED_RESULTS_FIELD: dataJsonList
    })


def GetFileResponse(request, filePath, filename):
    fileHandle = open(filePath, "rb")
    response = FileResponse(fileHandle, content_type=RESPONSE_FILE_CONTENT_TYPE_VALUE)
    response[RESPONSE_FILE_CONTENT_LENGTH_FIELD] = os.path.getsize(filePath)
    response[RESPONSE_FILE_CONTENT_DISPOSITION_FIELD] = RESPONSE_FILE_CONTENT_DISPOSITION_FILE_VALUE % filename
    return response