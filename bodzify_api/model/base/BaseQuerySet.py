from typing import Any, Dict, Type

from django.db import models

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
        return isinstance(field, models.CharField) and field.db_column == LibTrackMixinFields.NAME_PUBLIC
    except (models.FieldDoesNotExist, AttributeError):
        return False


class BaseQuerySet(models.QuerySet):
    """QuerySet that handles name field transformations for both direct and related fields."""

    def transform_internal_fields(self, **kwargs: Any) -> Dict[str, Any]:
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
            print(f"Processing key: {key}")
            print(f"NAME_PUBLIC value: {LibTrackMixinFields.NAME_PUBLIC!r}")
            print(f"Model: {self.model.__name__}")

            # Split the key into parts
            parts = key.split('__')
            print(f"Split parts: {parts}")

            # Find any part that starts with 'name'
            name_part_index = -1
            for i, part in enumerate(parts):
                if part.startswith(LibTrackMixinFields.NAME_PUBLIC):
                    name_part_index = i
                    break

            if name_part_index >= 0:
                print(f"Found name at index: {name_part_index}")
                # Get the model that owns the name field
                field_path = '__'.join(parts[:name_part_index]) if name_part_index > 0 else ''
                current_model = get_related_model(self.model, field_path) if field_path else self.model
                print(f"Current model: {current_model.__name__}")

                # Check if this model uses internal name fields
                uses_internal = uses_internal_name(current_model)
                print(f"Uses internal name: {uses_internal}")

                if uses_internal:
                    # Transform name to _name while preserving any suffixes
                    name_part = parts[name_part_index]
                    suffix = name_part[len(LibTrackMixinFields.NAME_PUBLIC):]  # Get any suffix after 'name'
                    parts[name_part_index] = LibTrackMixinFields.NAME_INTERNAL + suffix
                    transformed_key = '__'.join(parts)
                    print(f"Transformed to: {transformed_key}")
                    transformed[transformed_key] = value
                else:
                    transformed[key] = value
            else:
                transformed[key] = value

        return transformed

    def filter(self, *args: Any, **kwargs: Any) -> 'BaseQuerySet':
        print('kwargs', kwargs)
        transformed_kwargs = self.transform_internal_fields(**kwargs)
        print('transformed_kwargs', transformed_kwargs)
        return super().filter(*args, **transformed_kwargs)

    def exclude(self, *args: Any, **kwargs: Any) -> 'BaseQuerySet':
        transformed_kwargs = self.transform_internal_fields(**kwargs)
        return super().exclude(*args, **transformed_kwargs)

    def get(self, *args: Any, **kwargs: Any) -> Any:
        transformed_kwargs = self.transform_internal_fields(**kwargs)
        return super().get(*args, **transformed_kwargs)

    def create(self, **kwargs: Any) -> Any:
        transformed_kwargs = self.transform_internal_fields(**kwargs)
        return super().create(**transformed_kwargs)

    def get_or_create(self, **kwargs: Any) -> Any:
        transformed_kwargs = self.transform_internal_fields(**kwargs)
        return super().get_or_create(**transformed_kwargs)
