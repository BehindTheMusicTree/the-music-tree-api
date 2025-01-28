from typing import Any, Dict, Type

from django.db import models
from django.db.models import QuerySet

from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields


def get_related_model(model: Type[models.Model], field_path: str) -> Type[models.Model]:
    """
    Get the model class for a related field path.

    Args:
        model: The base model class to start from
        field_path: The field path (e.g., 'manual_playlist__name__icontains')

    Returns:
        The model class corresponding to the last valid model in the path
    """
    parts = field_path.split('__')
    current_model: Type[models.Model] = model

    for part in parts:
        # Skip lookup expressions
        if part in ['isnull', 'icontains', 'contains', 'startswith', 'endswith']:
            break

        try:
            field = current_model._meta.get_field(part)
            if hasattr(field, 'related_model') and field.related_model is not None:
                current_model = field.related_model
        except (models.FieldDoesNotExist, AttributeError):
            # If we hit an invalid field, stop traversing but return the last valid model
            break

    return current_model


def uses_internal_name(model: Type[models.Model]) -> bool:
    try:
        field = model._meta.get_field(LibTrackMixinFields.NAME_INTERNAL)
        return (isinstance(field, models.CharField) and
                field.db_column == LibTrackMixinFields.NAME_PUBLIC)
    except (models.FieldDoesNotExist, AttributeError):
        return False


class BaseQuerySet(models.QuerySet):
    """QuerySet that handles name field transformations for both direct and related fields."""

    def transform_related_fields(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Transform name fields in related field queries.

        This method handles both direct field references and related field queries like:
        - manual_playlist__name__icontains
        - related_model__name

        Args:
            **kwargs: The query parameters

        Returns:
            Dict with transformed field names
        """
        transformed = {}

        for key, value in kwargs.items():
            # Handle direct name field
            if key == LibTrackMixinFields.NAME_PUBLIC:
                if uses_internal_name(self.model):
                    transformed[LibTrackMixinFields.NAME_INTERNAL] = value
                else:
                    transformed[key] = value
            # Handle related name fields
            elif f'__{LibTrackMixinFields.NAME_PUBLIC}' in key:
                # Split on __name to preserve any lookups that come after
                parts = key.split(f'__{LibTrackMixinFields.NAME_PUBLIC}')
                field_path = parts[0]  # The path to the related model
                lookups = parts[1]     # Any trailing lookups (e.g., __icontains)

                # Get the model that owns the name field
                related_model = get_related_model(self.model, field_path)

                # Check if this model uses internal name fields
                if uses_internal_name(related_model):
                    # Transform name to _name while preserving the path and lookups
                    transformed_key = f"{field_path}__{LibTrackMixinFields.NAME_INTERNAL}{lookups}"
                    transformed[transformed_key] = value
                else:
                    transformed[key] = value
            else:
                transformed[key] = value

        return transformed

    def filter(self, *args: Any, **kwargs: Any) -> 'BaseQuerySet':
        transformed_kwargs = self.transform_related_fields(**kwargs)
        return super().filter(*args, **transformed_kwargs)

    def exclude(self, *args: Any, **kwargs: Any) -> 'BaseQuerySet':
        transformed_kwargs = self.transform_related_fields(**kwargs)
        return super().exclude(*args, **transformed_kwargs)

    def get(self, *args: Any, **kwargs: Any) -> Any:
        transformed_kwargs = self.transform_related_fields(**kwargs)
        return super().get(*args, **transformed_kwargs)

    def create(self, **kwargs: Any) -> Any:
        print('kwargs', kwargs)
        transformed_kwargs = self.transform_related_fields(**kwargs)
        print('transformed_kwargs', transformed_kwargs)
        return super().create(**transformed_kwargs)
