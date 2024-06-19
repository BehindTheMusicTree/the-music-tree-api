#!/usr/bin/env python

import os

from rest_framework import status
from rest_framework import exceptions
from rest_framework.pagination import PageNumberPagination

from django.db import IntegrityError
import django.views.defaults
from django.http import FileResponse
from rest_framework.response import Response
from django.core.paginator import Paginator


INTEGRITY_ERROR_MESSAGE = "There is an issue with the object sent"

RESPONSE_FILE_CONTENT_TYPE_VALUE = 'file'
RESPONSE_FILE_CONTENT_LEN_FIELD = 'Content-Length'
RESPONSE_FILE_CONTENT_DISPOSITION_FIELD = 'Content-Disposition'
RESPONSE_FILE_CONTENT_DISPOSITION_FILE_VALUE = 'attachment; filename="%s"'
RESPONSE_FILE_CONTENT_LEN_FIELD = 'Content-Length'

PAGINATED_COUNT_FIELD = "count"
PAGINATED_CURRENT_FIELD = "current"
PAGINATED_NEXT_FIELD = "next"
PAGINATED_PREVIOUS_FIELD = "previous"
PAGINATED_RESULTS_FIELD = "results"

REQUEST_QUERY_FIELD = "query"
REQUEST_PAGINATED_PAGE_FIELD = "page"
REQUEST_PAGINATED_PAGE_SIZE_FIELD = "pageSize"


def get_response_when_permission_denied(request):
    return django.views.defaults.permission_denied(request=request, exception=exceptions.PermissionDenied)


def get_response_when_bad_request(exception=exceptions.bad_request):
    if type(exception) == IntegrityError:
        errorMessage = INTEGRITY_ERROR_MESSAGE
    else:
        errorMessage = {}
        if isinstance(exception.detail, dict):
            for field, errors in exception.detail.items():
                errorMessage[field] = [str(error) for error in errors]
        else:
            errorMessage = {'error': str(exception.detail)}
    return Response(
        data={
            'status': '400',
            'message': 'Bad Request',
            'success': False,
            'errors': errorMessage
        },
        status=status.HTTP_400_BAD_REQUEST
    )


def get_json_response_paginated(request, data_json_list, headers=None):
    page_number = request.GET.get(REQUEST_PAGINATED_PAGE_FIELD, 0)
    paginator = Paginator(object_list=data_json_list, per_page=PageNumberPagination.page_size)
    page_object = paginator.get_page(page_number)

    return Response(
        headers=headers,
        data={
            PAGINATED_COUNT_FIELD: len(data_json_list),
            PAGINATED_CURRENT_FIELD: page_number,
            PAGINATED_NEXT_FIELD: page_object.has_next(),
            PAGINATED_PREVIOUS_FIELD: page_object.has_previous(),
            PAGINATED_RESULTS_FIELD: data_json_list
        })


def get_file_response(filePath, filename):
    fileHandle = open(filePath, "rb")
    response = FileResponse(fileHandle, content_type=RESPONSE_FILE_CONTENT_TYPE_VALUE)
    response[RESPONSE_FILE_CONTENT_LEN_FIELD] = os.path.getsize(filePath)
    response[RESPONSE_FILE_CONTENT_DISPOSITION_FIELD] = (RESPONSE_FILE_CONTENT_DISPOSITION_FILE_VALUE % filename)
    return response
