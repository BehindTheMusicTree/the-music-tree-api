from django_filters.rest_framework import DjangoFilterBackend

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException


class ConsistentParametersFilterBackend(DjangoFilterBackend):
    """
    Custom filter backend that ensures consistent parameter handling with pagination.

    Django REST Framework normally normalizes absent parameters to empty strings when 
    pagination is used. This backend prevents that behavior, ensuring that absent 
    parameters are consistently handled whether pagination is used or not.
    """

    def get_query_params(self, request):
        """Get query parameters in a way that works with both DRF Request and Django WSGIRequest"""
        if hasattr(request, 'query_params'):
            return request.query_params
        elif hasattr(request, 'GET'):
            return request.GET
        return {}

    def get_filterset_kwargs(self, request, queryset, view):
        query_params = self.get_query_params(request)

        original_query_params = set(request.GET.keys() if hasattr(request, 'GET') else request.query_params.keys())

        # Reimplement parent's get_filterset_kwargs logic to avoid accessing request.query_params directly
        kwargs = {
            'data': query_params.copy(),  # Use copy to avoid modifying the original
            'queryset': queryset,
            'request': request,
        }

        filterset_class = view.filterset_class if hasattr(view, 'filterset_class') else None

        for field_name in list(kwargs['data'].keys()):
            if field_name not in ['page', 'page_size']:
                if field_name not in original_query_params:
                    del kwargs['data'][field_name]
                else:
                    if not filterset_class:
                        raise AppValidationException(
                            field_name=field_name,
                            field_validation_error_code=FieldValidationErrorCode.INVALID_FILTER,
                            message=f"Filter is not valid")

        return kwargs

    def get_schema_operation_parameters(self, view):
        """
        Return parameters for OpenAPI schema generation.
        Delegates to parent class implementation for drf-spectacular compatibility.
        """
        if hasattr(super(), 'get_schema_operation_parameters'):
            return super().get_schema_operation_parameters(view)
        return []
