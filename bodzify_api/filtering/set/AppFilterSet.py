from django_filters import FilterSet
from bodzify_api.utils import data_transformer
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


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
            raise_validation_error(
                message=f'Invalid filter(s) detected: {", ".join(sorted(invalid_filters))}',
                code=FieldValidationErrorCode.FIELD_INVALID_FILTER.value,
                field='filters'
            )

        return super(AppFilterSet, self).qs
