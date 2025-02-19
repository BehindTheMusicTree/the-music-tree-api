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
            if len(invalid_filters) == 1:
                raise AppValidationError(
                    field_name=f'{invalid_filters[0]}',
                    message=f'Invalid filter detected',
                    field_validation_error_code=FieldValidationErrorCode.INVALID_FILTER
                )
            raise AppValidationError(
                field_name=f'{", ".join(sorted(invalid_filters))}',
                message=f'Invalid filters detected',
                field_validation_error_code=FieldValidationErrorCode.INVALID_FILTERS
            )

        return super(AppFilterSet, self).qs
