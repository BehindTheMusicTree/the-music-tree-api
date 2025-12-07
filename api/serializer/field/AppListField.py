from typing import Any

from rest_framework.fields import ListField

from api.serializer.field.AppField import AppField


class AppListField(AppField, ListField):
    def __init__(self, **kwargs):
        ListField.__init__(self, **kwargs)
        self._child_field = None

    @property
    def child_field(self) -> Any:
        return self.child

    def get_error_field_name(self) -> str:
        return self.field_name or "list"

    def to_internal_value(self, data: Any) -> Any:
        if data is None:
            if not self.allow_null:
                self.fail('null')
            return None

        if not data:
            if not self.allow_empty:
                self.fail('required')
            return []

        if not isinstance(data, list):
            self.fail('not_a_list')

        return super().to_internal_value(data)
