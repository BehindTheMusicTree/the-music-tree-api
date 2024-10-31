
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination

from bodzify_api import settings


class DefaultMultipleModelLimitOffsetPagination(MultipleModelLimitOffsetPagination):
    default_limit = settings.PAGINATION_LIMIT_OFFSET_DEFAULT
