
from django.core.exceptions import ImproperlyConfigured
from django_filters import Filter, FilterSet


class AppFilter(Filter):
    field_name_public: str | None

    def __init__(self, field_name_public: str | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_name_public = field_name_public

        if self.field_name and not self.field_name_public:
            raise ImproperlyConfigured('field_name_public must be provided when field_name is set')

    def is_param_in_request(self) -> bool:
        """
        Check if this filter's parameter is actually in the URL request.
        Returns True if the parameter is in the request, False otherwise.
        """
        parent: FilterSet | None = getattr(self, 'parent', None)
        if not parent:
            return True  # If no parent, assume parameter is present

        # If we have a request, check if this parameter is in the original URL params
        if hasattr(parent, 'request') and parent.request:
            original_params = parent.request.GET if hasattr(parent.request, 'GET') else parent.request.query_params
            field_name = self.field_name_public or self.field_name
            return field_name in original_params

        return True  # If no request, assume parameter is present

    def filter(self, queryset, value):
        """
        Generic filter method for all filters.
        - Returns unfiltered queryset if value is None
        - For empty strings, checks if the parameter is in the URL before filtering
        """
        # Don't filter if value is None
        if value is None:
            return queryset

        # For empty strings, check if the parameter was actually in the URL
        if value == '' and not self.is_param_in_request():
            # Parameter wasn't in the URL, so don't filter
            return queryset

        # Call the parent class implementation for actual filtering
        return super().filter(queryset, value)
