
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination

from api import settings


class DefaultMultipleModelLimitOffsetPagination(MultipleModelLimitOffsetPagination):
    default_limit = settings.PAGINATION_PAGE_SIZE_MULTIMODEL_DEFAULT
