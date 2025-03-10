
class JsonDuplicateKeyTracker:

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
