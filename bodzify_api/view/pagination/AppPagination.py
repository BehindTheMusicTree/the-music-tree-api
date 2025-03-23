from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from bodzify_api import settings

from .PaginatedResponseFields import PaginatedResponseFields


class AppPagination(PageNumberPagination):
    page_size: int = settings.PAGINATION_PAGE_SIZE_DEFAULT
    page_size_query_param = 'page_size'
    max_page_size = settings.PAGINATION_PAGE_SIZE_MAX

    def get_paginated_response(self, data):
        # Check if pagination has been performed
        if not hasattr(self, 'page') or self.page is None:
            return Response({
                PaginatedResponseFields.OVERALL_TOTAL: 0,
                PaginatedResponseFields.NEXT: None,
                PaginatedResponseFields.PREVIOUS: None,
                PaginatedResponseFields.RESULTS: data,
                PaginatedResponseFields.PAGE: 1,
                PaginatedResponseFields.PAGE_SIZE: self.page_size,
                PaginatedResponseFields.TOTAL_PAGES: 0
            })

        # Calculate total pages using safe integer operations
        count = self.count
        page_size = int(self.page_size)
        total_pages = ((count + page_size - 1) // page_size) if count > 0 else 0

        # Normal pagination response
        return Response({
            PaginatedResponseFields.OVERALL_TOTAL: count,
            PaginatedResponseFields.NEXT: self.get_next_link(),
            PaginatedResponseFields.PREVIOUS: self.get_previous_link(),
            PaginatedResponseFields.RESULTS: data,
            PaginatedResponseFields.PAGE: self.page.number,
            PaginatedResponseFields.PAGE_SIZE: page_size,
            PaginatedResponseFields.TOTAL_PAGES: total_pages
        })

    @property
    def count(self) -> int:
        """Get total count of items across all pages with null safety"""
        if not hasattr(self, 'page') or self.page is None:
            return 0
        if not hasattr(self.page, 'paginator'):
            return 0
        return getattr(self.page.paginator, 'count', 0)
