from django_filters.rest_framework import DjangoFilterBackend


class ConsistentParametersFilterBackend(DjangoFilterBackend):
    """
    Custom filter backend that ensures consistent parameter handling with pagination.

    Django REST Framework normally normalizes absent parameters to empty strings when 
    pagination is used. This backend prevents that behavior, ensuring that absent 
    parameters are consistently handled whether pagination is used or not.
    """

    def get_filterset_kwargs(self, request, queryset, view):
        """
        Get the arguments to pass to the filterset class constructor.

        This overrides the parent method to modify how request parameters are processed
        when pagination is involved.
        """
        # Get standard kwargs from parent method
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # If pagination parameters are present, process the data to prevent normalization
        if any(param in request.query_params for param in ['page', 'pageSize']):
            # Create filterset instance to safely access filter fields
            filterset_class = self.get_filterset_class(view, queryset)
            if filterset_class:
                # Get filter fields from filterset meta or model fields if available
                filter_fields = []

                # Try to get fields from Meta class
                if hasattr(filterset_class, 'Meta') and hasattr(filterset_class.Meta, 'fields'):
                    if isinstance(filterset_class.Meta.fields, dict):
                        filter_fields = list(filterset_class.Meta.fields.keys())
                    else:
                        filter_fields = list(filterset_class.Meta.fields)

                # For each parameter that might be a filter field
                for field_name in list(kwargs['data'].keys()):
                    # If it looks like a filter field and wasn't in the original request
                    if (field_name not in ['page', 'pageSize'] and
                        field_name not in request.query_params and
                            kwargs['data'].get(field_name, '') == ''):
                        # Remove it to ensure consistent behavior
                        del kwargs['data'][field_name]

        return kwargs
