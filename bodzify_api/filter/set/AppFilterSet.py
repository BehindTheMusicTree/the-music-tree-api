
from django_filters import FilterSet
from rest_framework.exceptions import ValidationError

from bodzify_api.model.user.User import User
from bodzify_api.utils.utils import to_camel_case


class AppFilterSet(FilterSet):

    def __init__(self, data=None, *args, **kwargs):
        print(f"[DEBUG] AppFilterSet.__init__ data={data}")
        super().__init__(data=data, *args, **kwargs)

    @property
    def qs(self):
        """
        Override the qs property to add validation of filter parameters.
        Raises ValidationError if any filter parameter is not declared in the FilterSet.
        """
        # Get all declared filters
        valid_filters = set(self.filters.keys())
        print(f"[DEBUG] Valid filters: {valid_filters}")
        print(f"[DEBUG] Data keys: {self.data.keys() if self.data else 'None'}")

        # Check received parameters against valid filters
        invalid_filters = []
        for param in self.data.keys():
            if param not in valid_filters:
                invalid_filters.append(to_camel_case(param))

        if invalid_filters:
            invalid_filters_str = ', '.join(invalid_filters)
            raise ValidationError(f"Invalid filter(s): {invalid_filters_str}")

        return super().qs
