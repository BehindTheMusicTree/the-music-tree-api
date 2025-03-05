from json import JSONEncoder
from typing import Any
from uuid import UUID


def transform_uuids(obj: Any) -> Any:
    """Transform UUID objects in a data structure to their string representation.

    This function walks through dictionaries, lists, and other data structures,
    converting any UUID objects to strings while preserving all other data types.

    Args:
        obj: The object to transform. Can be a dictionary, list, UUID, or any other type.

    Returns:
        The transformed object with all UUIDs converted to strings.
    """
    if isinstance(obj, dict):
        return {key: transform_uuids(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [transform_uuids(item) for item in obj]
    elif isinstance(obj, UUID):
        return str(obj)
    return obj


class UUIDJSONEncoder(JSONEncoder):
    """JSON encoder that can handle UUID objects by converting them to strings.

    This encoder extends the standard JSONEncoder to add support for UUID serialization.
    It converts UUID objects to their string representation while maintaining default
    behavior for all other types.
    """

    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)
