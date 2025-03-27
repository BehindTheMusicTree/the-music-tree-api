from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from bodzify_api import settings

from .PaginatedResponseFields import PaginatedResponseFields


class AppPagination(PageNumberPagination):
    page_size: int = settings.PAGINATION_PAGE_SIZE_DEFAULT
    page_size_query_param = 'page_size'
    max_page_size = settings.PAGINATION_PAGE_SIZE_MAX

    def get_page_number(self, request, paginator):
        """
        Override to return 400 Bad Request for invalid page numbers
        instead of 404 Not Found.
        """
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        try:
            # Convert to integer, raising proper exception if not valid
            page_number = int(page_number)
            if page_number < 1:
                from rest_framework.exceptions import ParseError
                # Use ParseError with a string argument for the detail field
                raise ParseError("Invalid page.")
        except (TypeError, ValueError):
            from rest_framework.exceptions import ParseError
            # Use ParseError with a string argument for the detail field
            raise ParseError("Invalid page.")

        return page_number

    def get_page_size(self, request):
        """
        Get the page size from request.
        Support both 'page_size' and 'pageSize' parameters for backwards compatibility.
        """
        # Default to the configured page size
        page_size = self.page_size

        if request is not None:
            # Try snake_case parameter first (standard)
            if self.page_size_query_param in request.query_params:
                try:
                    param_value = request.query_params[self.page_size_query_param]
                    page_size = int(param_value)
                except (ValueError, TypeError):
                    pass

            # If not found, try camelCase parameter (for backward compatibility)
            elif 'pageSize' in request.query_params:
                try:
                    param_value = request.query_params['pageSize']
                    page_size = int(param_value)
                except (ValueError, TypeError):
                    pass

        # Ensure page size doesn't exceed the maximum
        if self.max_page_size and page_size > self.max_page_size:
            return self.max_page_size

        return page_size

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

        # Get the actual page size used for this request
        if hasattr(self, 'request') and self.request is not None:
            requested_page_size = self.get_page_size(self.request)
            page_size = int(requested_page_size) if requested_page_size is not None else int(self.page_size)
        else:
            # Fallback to paginator's per_page or the default page size
            page_size = int(self.page.paginator.per_page) if hasattr(self.page, 'paginator') else int(self.page_size)

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
