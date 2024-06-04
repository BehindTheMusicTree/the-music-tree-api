#!/usr/bin/env python

from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from rest_framework.response import Response

from bodzify_api.settings import settings


class DefaultMultipleModelLimitOffsetPagination(MultipleModelLimitOffsetPagination):
    default_limit = settings.PAGINATION_LIMIT_OFFSET_DEFAULT
