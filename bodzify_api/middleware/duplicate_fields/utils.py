import json


class DuplicateKeyTracker:
    """Track duplicate keys during JSON parsing."""

    def __init__(self):
        self.seen_keys = {}
        self.duplicates = []

    def check_key(self, key: str, path: str = '') -> None:
        """Check if a key is duplicate at its current path."""
        full_path = f"{path}.{key}" if path else key
        if full_path in self.seen_keys:
            if full_path not in self.duplicates:
                self.duplicates.append(key)
        else:
            self.seen_keys[full_path] = True


class DuplicateDetectingDecoder(json.JSONDecoder):
    """Custom JSON decoder that detects duplicate keys during parsing."""

    def __init__(self, *args, **kwargs):
        self.tracker = DuplicateKeyTracker()
        json.JSONDecoder.__init__(self, object_pairs_hook=self.object_pairs_hook, *args, **kwargs)

    def object_pairs_hook(self, pairs):
        """Process key-value pairs during JSON parsing."""
        for key, _ in pairs:
            self.tracker.check_key(key)
        return dict(pairs)


def find_duplicate_fields(json_str: str) -> list[str]:
    """Find duplicate fields in a JSON object, detecting duplicates during parsing."""
    try:
        decoder = DuplicateDetectingDecoder()
        decoder.decode(json_str)
        return decoder.tracker.duplicates
    except json.JSONDecodeError:
        return []