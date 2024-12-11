from django_filters import FilterSet
from rest_framework.exceptions import ValidationError
from bodzify_api.utils import data_transformer
from bodzify_api.utils.validation_error_utils import raise_validation_error


class AppFilterSet(FilterSet):
    """Base filter set class with validation for unknown filters."""
    strict = False

    @property
    def qs(self):
        """
        Override the qs property to add validation of filter parameters.
        Raises ValidationError if any filter parameter is not declared in the FilterSet.
        """
        valid_filters = set(self.filters.keys())
        invalid_filters = []

        for param in self.data.keys():
            if param not in valid_filters:
                invalid_filters.append(data_transformer.to_camel_case(param))

        if invalid_filters:
            raise_validation_error(
                message=f'Invalid filter(s) detected: {", ".join(sorted(invalid_filters))}',
                code='invalid_filters',
                field='filters'
            )

        return super(AppFilterSet, self).qs
