
import json

from .JsonDuplicateKeyTracker import JsonDuplicateKeyTracker


class JsonDuplicateKeyDetectingDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        self.tracker = JsonDuplicateKeyTracker()
        json.JSONDecoder.__init__(self, object_pairs_hook=self.object_pairs_hook, *args, **kwargs)

    def object_pairs_hook(self, pairs):
        for key, _ in pairs:
            self.tracker.check_key(key)
        return dict(pairs)
