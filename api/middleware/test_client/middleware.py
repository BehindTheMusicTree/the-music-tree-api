from typing import Union

from django.http import HttpRequest, HttpResponse, JsonResponse, QueryDict
from rest_framework.request import Request


class TestClientEmptyListMiddleware:
    """
    Middleware to handle empty list conversion for test client requests.

    DRF's test client may drop empty lists in multipart form data, so we convert
    [] to [''] for list fields (with [] suffix) to ensure the field is preserved.
    This conversion happens in the test client, and this middleware normalizes
    [''] back to [] during request processing.

    This middleware only processes requests marked with X-Test-Client header.
    For POST requests, it normalizes request.POST directly (after CamelToSnakeMiddleware).
    For PUT/PATCH requests, normalization is handled in AppInputSerializer because
    accessing request.data in middleware triggers DRF parsing, but overriding it
    is unreliable due to DRF's internal caching mechanism.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Union[HttpRequest, Request]) -> Union[HttpResponse, JsonResponse]:
        is_test_client = request.META.get('HTTP_X_TEST_CLIENT') == 'true'

        if is_test_client and request.method == 'POST':
            content_type = request.content_type or ''

            if content_type.startswith('multipart/form-data'):
                # For POST requests, Django populates request.POST
                # CamelToSnakeMiddleware has already converted it to snake_case
                if hasattr(request, 'POST') and isinstance(request.POST, QueryDict):
                    request.POST = self._normalize_empty_lists(request.POST)  # type: ignore

        response = self.get_response(request)
        return response

    def _normalize_empty_lists(self, post_data: QueryDict) -> QueryDict:
        """Normalize [''] back to [] for list fields (with [] suffix).

        Test client converts [] to [''] to preserve fields, but we want to
        normalize [''] back to [] so field validation sees empty lists correctly.
        """
        if not isinstance(post_data, QueryDict):
            return post_data

        result = QueryDict(mutable=True)

        for key, values in post_data.lists():
            # For list fields (with [] suffix), convert [''] back to []
            if key.endswith('[]') and values == ['']:
                result.setlist(key, [])
            else:
                result.setlist(key, values)

        return result
