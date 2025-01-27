from typing import Any, Dict, Type

from django.core.exceptions import FieldDoesNotExist
from django.db import models

from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields


def uses_internal_name(model: Type[models.Model]) -> bool:
    """Check if a model actually uses internal name fields."""
    try:
        # Check if model has _name field
        field = model._meta.get_field(LibTrackMixinFields.NAME_INTERNAL)
        # Verify it's a CharField with db_column='name'
        return (isinstance(field, models.CharField) and
                field.db_column == LibTrackMixinFields.NAME_PUBLIC)
    except FieldDoesNotExist:
        return False


def transform_name_fields(model: Type[models.Model], **kwargs: Any) -> Dict[str, Any]:
    """
    Transform name fields to internal name fields in all cases:
    - Direct field references (name → _name)
    - Relationship traversals (criteria__name → criteria___name)
    - Complex lookups (criteria__name__icontains → criteria___name__icontains)
    """
    transformed = {}

    for key, value in kwargs.items():
        # Handle direct name field references
        if key == LibTrackMixinFields.NAME_PUBLIC and uses_internal_name(model):
            transformed[LibTrackMixinFields.NAME_INTERNAL] = value
        # Handle relationship traversals and lookups containing __name
        elif '__' + LibTrackMixinFields.NAME_PUBLIC in key:
            # Split on __name to preserve any lookups that come after
            parts = key.split('__' + LibTrackMixinFields.NAME_PUBLIC)
            if len(parts) == 2:
                # parts[0] is the relationship path
                # parts[1] is either empty or contains lookups (like __icontains)
                transformed[parts[0] + '__' + LibTrackMixinFields.NAME_INTERNAL + parts[1]] = value
            else:
                transformed[key] = value
        else:
            transformed[key] = value

    return transformed


def update_name_field(instance: models.Model, name_value: str) -> None:
    """
    Update the name field directly in the database, handling both the instance
    and any self-referential root records.

    Args:
        instance: The model instance to update
        name_value: The new name value to set
    """
    if not uses_internal_name(instance.__class__):
        return

    # Update the instance's name in the database
    type(instance).objects.filter(pk=instance.pk).update(**{
        LibTrackMixinFields.NAME_INTERNAL: name_value
    })

    # Handle self-referential root records
    root = getattr(instance, 'root', None)
    if root is not None and root == instance:
        root_pk = getattr(root, 'pk', None)
        if root_pk is not None:
            type(instance).objects.filter(pk=root_pk).update(**{
                LibTrackMixinFields.NAME_INTERNAL: name_value
            })
