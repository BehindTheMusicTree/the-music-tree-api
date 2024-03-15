#!/usr/bin/env python

from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from rest_framework.response import Response

import bodzify_api.settings as settings


class DefaultMultipleModelLimitOffsetPagination(MultipleModelLimitOffsetPagination):
    default_limit = settings.PAGINATION_LIMIT_OFFSET_DEFAULT
