
from django.utils.translation import gettext as _
from django_filters.filterset import FilterSet

from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter
from api.model.base.BaseQuerySet import BaseQuerySet


class NonEmptiableCharFilter(EmptiableCharFilter):
    parent: FilterSet

    def filter(self, qs: BaseQuerySet, value: str) -> BaseQuerySet:
        parent_data = getattr(self.parent, 'data', {})

        if (self.field_name_public or self.field_name) in parent_data:
            if value == '':
                raise AppValidationException(
                    field_name=str(self.field_name_public or self.field_name),
                    message=_('This field may not be blank.'),
                    field_validation_error_code=FieldValidationErrorCode.BLANK
                )
            return super().filter(qs, value)
        return qs
