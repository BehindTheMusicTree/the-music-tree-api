from typing import Any, Type

from django.core.exceptions import FieldDoesNotExist
from django.db import models

from .Fields import Fields


def uses_internal_name(model: Type[models.Model]) -> bool:
    try:
        field = model._meta.get_field(Fields.NAME_INTERNAL)
        # Verify it's a CharField with db_column='name'
        return (isinstance(field, models.CharField) and
                field.db_column == Fields.NAME_PUBLIC)
    except FieldDoesNotExist:
        return False


def transform_name_fields(model: Type[models.Model], **kwargs: Any) -> dict[str, Any]:
    """
    Transform name fields to internal name fields in all cases:
    - Direct field references (name → _name)
    - Relationship traversals (criteria__name → criteria___name)
    - Complex lookups (criteria__name__icontains → criteria___name__icontains)
    """
    transformed = {}

    for key, value in kwargs.items():
        # Handle direct name field references
        if key == Fields.NAME_PUBLIC and uses_internal_name(model):
            transformed[Fields.NAME_INTERNAL] = value
        # Handle relationship traversals and lookups containing __name
        elif '__' + Fields.NAME_PUBLIC in key:
            # Split on __name to preserve any lookups that come after
            parts = key.split('__' + Fields.NAME_PUBLIC)
            if len(parts) == 2:
                # parts[0] is the relationship path
                # parts[1] is either empty or contains lookups (like __icontains)
                transformed[parts[0] + '__' + Fields.NAME_INTERNAL + parts[1]] = value
            else:
                transformed[key] = value
        else:
            transformed[key] = value

    return transformed
