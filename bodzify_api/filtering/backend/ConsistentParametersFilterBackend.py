from django_filters.rest_framework import DjangoFilterBackend


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

        for field_name in list(kwargs['data'].keys()):
            if field_name not in ['page', 'page_size'] and field_name not in original_query_params:
                del kwargs['data'][field_name]

        return kwargs
