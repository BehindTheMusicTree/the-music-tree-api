from django_filters import FilterSet
from bodzify_api.utils import data_transformer
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class AppFilterSet(FilterSet):
    strict = False

    @property
    def qs(self):
        valid_filters = set(self.filters.keys())
        invalid_filters = []

        for param in self.data.keys():
            if param not in valid_filters:
                invalid_filters.append(data_transformer.to_camel_case(param))

        if invalid_filters:
            raise AppValidationError.from_filterset(
                field=f'{", ".join(sorted(invalid_filters))}',
                message=f'Invalid filter(s) detected: {", ".join(sorted(invalid_filters))}',
                code=FieldValidationErrorCode.INVALID_FILTER
            )

        return super(AppFilterSet, self).qs
