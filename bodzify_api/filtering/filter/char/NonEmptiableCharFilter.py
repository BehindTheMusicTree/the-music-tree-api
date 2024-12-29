from rest_framework.exceptions import ValidationError

from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter


class NonEmptiableCharFilter(EmptiableCharFilter):

    def filter(self, qs, value):
        if not value:
            print(self.field_name)
            raise ValidationError({self.field_name_user_friendly or self.field_name: "The field cannot be empty"})
        return super().filter(qs, value)
