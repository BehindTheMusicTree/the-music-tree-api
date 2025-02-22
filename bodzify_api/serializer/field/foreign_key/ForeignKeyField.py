from typing import Any

from rest_framework.relations import PrimaryKeyRelatedField

from bodzify_api.serializer.field.AppField import AppField


class ForeignKeyField(AppField, PrimaryKeyRelatedField):
    """
    Custom ForeignKey serializer field that raises AppValidationError instead of DRF's ValidationError.
    This ensures consistent error handling across the application.

    Supports additional filters for validation:
        track = ForeignKeyField(
            queryset=LibraryTrack.objects.all(),
            additional_filters={'user': request.user}
        )
    """

    def __init__(self, **kwargs):
        self.additional_filters = kwargs.pop('additional_filters', {})
        super().__init__(**kwargs)

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        if self.additional_filters:
            queryset = queryset.filter(**self.additional_filters)
        return queryset

    def to_internal_value(self, data: Any) -> Any:
        return PrimaryKeyRelatedField.to_internal_value(self, data)
