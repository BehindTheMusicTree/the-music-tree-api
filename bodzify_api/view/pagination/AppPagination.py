from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from bodzify_api import settings

from .PaginatedResponseFields import PaginatedResponseFields


class AppPagination(PageNumberPagination):
    page_size = settings.PAGINATION_PAGE_SIZE_DEFAULT
    page_size_query_param = 'page_size'
    max_page_size = settings.PAGINATION_PAGE_SIZE_MAX

    def get_paginated_response(self, data):
        return Response({
            PaginatedResponseFields.OVERALL_TOTAL: self.count,
            PaginatedResponseFields.NEXT: self.get_next_link(),
            PaginatedResponseFields.PREVIOUS: self.get_previous_link(),
            PaginatedResponseFields.RESULTS: data
        })

    @property
    def count(self) -> int:
        """Get total count of items across all pages with null safety"""
        if not hasattr(self, 'page') or self.page is None:
            return 0
        if not hasattr(self.page, 'paginator'):
            return 0
        return getattr(self.page.paginator, 'count', 0)
