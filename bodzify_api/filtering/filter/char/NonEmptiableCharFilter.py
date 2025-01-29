
from django.db.models import QuerySet
from django.utils.translation import gettext as _
from django_filters.filterset import FilterSet

from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.ValidationResponseCode import ValidationResponseCode


class NonEmptiableCharFilter(EmptiableCharFilter):
    parent: FilterSet

    def filter(self, qs: QuerySet, value: str) -> QuerySet:
        parent_data = getattr(self.parent, 'data', {})

        if (self.field_name_user_friendly or self.field_name) in parent_data:
            if value == '':
                raise_validation_error(
                    message=_('This field may not be blank.'),
                    code=ValidationResponseCode.FIELD_BLANK.value,
                    field=str(self.field_name_user_friendly or self.field_name)
                )

        result = super().filter(qs, value)
        return result
