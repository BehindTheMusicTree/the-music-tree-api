from typing import Any, Dict, Type

from django.db import models
from django.db.models import Q

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
    """QuerySet that handles name field transformations for both direct and related fields, including Q objects."""

    def transform_q_object(self, q_object: Q) -> Q:
        """
        Transform field names in a Q object recursively.

        Args:
            q_object: The Q object to transform

        Returns:
            A new Q object with transformed field names
        """
        # New Q object to hold transformed conditions
        new_q = Q()
        new_q.connector = q_object.connector
        new_q.negated = q_object.negated

        # Transform each child
        for child in q_object.children:
            if isinstance(child, Q):
                # Recursively transform nested Q objects
                new_q.children.append(self.transform_q_object(child))
            else:
                # Transform (key, value) tuples
                key, value = child
                transformed_kwargs = self.transform_keyword_internal_fields(**{key: value})
                if transformed_kwargs:
                    # Get the first (and only) item from transformed_kwargs
                    transformed_key = next(iter(transformed_kwargs.keys()))
                    transformed_value = transformed_kwargs[transformed_key]
                    new_q.children.append((transformed_key, transformed_value))
                else:
                    new_q.children.append(child)

        return new_q

    def transform_q_objects_internal_fields(self, *args: Any) -> tuple:
        """
        Transform Q objects in args.

        Args:
            *args: Query arguments that may contain Q objects

        Returns:
            Tuple of transformed arguments
        """
        transformed_args = []
        for arg in args:
            if isinstance(arg, Q):
                transformed_args.append(self.transform_q_object(arg))
            else:
                transformed_args.append(arg)
        return tuple(transformed_args)

    def transform_keyword_internal_fields(self, **kwargs: Any) -> Dict[str, Any]:
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

            # Split the key into parts
            parts = key.split('__')

            # Find any part that starts with 'name'
            name_part_index = -1
            for i, part in enumerate(parts):
                if part.startswith(LibTrackMixinFields.NAME_PUBLIC):
                    name_part_index = i
                    break

            if name_part_index >= 0:
                # Get the model that owns the name field
                field_path = '__'.join(parts[:name_part_index]) if name_part_index > 0 else ''
                current_model = get_related_model(self.model, field_path) if field_path else self.model

                # Check if this model uses internal name fields
                uses_internal = uses_internal_name(current_model)

                if uses_internal:
                    # Transform name to _name while preserving any suffixes
                    name_part = parts[name_part_index]
                    suffix = name_part[len(LibTrackMixinFields.NAME_PUBLIC):]  # Get any suffix after 'name'
                    parts[name_part_index] = LibTrackMixinFields.NAME_INTERNAL + suffix
                    transformed_key = '__'.join(parts)
                    transformed[transformed_key] = value
                else:
                    transformed[key] = value
            else:
                transformed[key] = value

        return transformed

    def filter(self, *args: Any, **kwargs: Any) -> 'BaseQuerySet':
        transformed_args = self.transform_q_objects_internal_fields(*args)
        transformed_kwargs = self.transform_keyword_internal_fields(**kwargs)
        return super().filter(*transformed_args, **transformed_kwargs)

    def exclude(self, *args: Any, **kwargs: Any) -> 'BaseQuerySet':
        transformed_args = self.transform_q_objects_internal_fields(*args)
        transformed_kwargs = self.transform_keyword_internal_fields(**kwargs)
        return super().exclude(*transformed_args, **transformed_kwargs)

    def get(self, *args: Any, **kwargs: Any) -> Any:
        transformed_args = self.transform_q_objects_internal_fields(*args)
        transformed_kwargs = self.transform_keyword_internal_fields(**kwargs)
        return super().get(*transformed_args, **transformed_kwargs)

    def create(self, **kwargs: Any) -> Any:
        transformed_kwargs = self.transform_keyword_internal_fields(**kwargs)
        return super().create(**transformed_kwargs)

    def get_or_create(self, **kwargs: Any) -> Any:
        transformed_kwargs = self.transform_keyword_internal_fields(**kwargs)
        return super().get_or_create(**transformed_kwargs)
