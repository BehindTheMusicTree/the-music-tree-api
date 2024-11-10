from django_filters import FilterSet
from rest_framework.exceptions import ValidationError

from bodzify_api.utils import data_transformer


class AppFilterSet(FilterSet):

    @property
    def qs(self):
        """
        Override the qs property to add validation of filter parameters.
        Raises ValidationError if any filter parameter is not declared in the FilterSet.
        """
        # Get all declared filters
        valid_filters = set(self.filters.keys())

        # Check received parameters against valid filters
        invalid_filters = []
        for param in self.data.keys():
            if param not in valid_filters:
                invalid_filters.append(data_transformer.to_camel_case(param))

        if invalid_filters:
            invalid_filters_str = ', '.join(invalid_filters)
            raise ValidationError(f"Invalid filter(s): {invalid_filters_str}")

        return super().qs
