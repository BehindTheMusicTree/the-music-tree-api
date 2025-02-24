
import json

from bodzify_api.middleware.duplicate_fields.JsonDuplicateKeyTracker import JsonDuplicateKeyTracker


class JsonDuplicateDetectingDecoder(json.JSONDecoder):
    """Custom JSON decoder that detects duplicate keys during parsing."""

    def __init__(self, *args, **kwargs):
        self.tracker = JsonDuplicateKeyTracker()
        json.JSONDecoder.__init__(self, object_pairs_hook=self.object_pairs_hook, *args, **kwargs)

    def object_pairs_hook(self, pairs):
        """Process key-value pairs during JSON parsing."""
        for key, _ in pairs:
            self.tracker.check_key(key)
        return (pairs)
