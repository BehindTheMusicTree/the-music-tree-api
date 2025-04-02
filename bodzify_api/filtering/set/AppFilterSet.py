from django_filters import FilterSet

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.base.BaseQuerySet import BaseQuerySet
from bodzify_api.utils import data_transformer


class AppFilterSet(FilterSet):
    # Pagination parameters that should not be considered as filters
    allowed_non_filter_params = {'page', 'page_size'}
    strict = False

    @property
    def qs(self):
        valid_filters = set(self.filters.keys())
        invalid_filters = []

        for param in self.data.keys():
            if param not in valid_filters and param not in self.allowed_non_filter_params:
                invalid_filters.append(data_transformer.to_camel_case(param))

        if invalid_filters:
            if len(invalid_filters) == 1:
                raise AppValidationException(field_name=f'{invalid_filters[0]}',
                                             message=f'Invalid filter detected',
                                             field_validation_error_code=FieldValidationErrorCode.INVALID_FILTER)

            raise AppValidationException(field_name=f'{", ".join(sorted(invalid_filters))}',
                                         message=f'Invalid filters detected',
                                         field_validation_error_code=FieldValidationErrorCode.INVALID_FILTERS)

        queryset = super().qs
        if not isinstance(queryset, BaseQuerySet):
            # If the queryset isn't already a BaseQuerySet, create one
            queryset = BaseQuerySet(queryset.model, using=queryset.db)
        return queryset
