from json import JSONEncoder
from uuid import UUID


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