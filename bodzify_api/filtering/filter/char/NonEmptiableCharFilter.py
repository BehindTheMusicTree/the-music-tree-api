
from bodzify_api.model.base.BaseQuerySet import BaseQuerySet
from django.utils.translation import gettext as _
from django_filters.filterset import FilterSet

from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter
from bodzify_api.view.error.AppValidationError import AppValidationError
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


class NonEmptiableCharFilter(EmptiableCharFilter):
    parent: FilterSet

    def filter(self, qs: BaseQuerySet, value: str) -> BaseQuerySet:
        parent_data = getattr(self.parent, 'data', {})

        if (self.field_name_user_friendly or self.field_name) in parent_data:
            if value == '':
                # Since this is field validation, use from_field
                raise AppValidationError.from_field(
                    field=str(self.field_name_user_friendly or self.field_name),
                    message=_('This field may not be blank.'),
                    code=FieldValidationErrorCode.FIELD_BLANK
                )

        result = super().filter(qs, value)
        return result
