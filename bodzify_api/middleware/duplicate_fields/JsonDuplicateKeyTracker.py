class JsonDuplicateKeyTracker:

    def __init__(self):
        self.object_stack = []  # Stack to track current object context
        self.duplicates = []

    def check_key(self, key: str) -> None:
        """Check if a key is duplicate within the current object context."""
        if not self.object_stack:
            return

        current_object = self.object_stack[-1]
        if key in current_object:
            if key not in self.duplicates:
                self.duplicates.append(key)
        else:
            current_object.add(key)

    def enter_object(self) -> None:
        """Called when entering a new object context."""
        self.object_stack.append(set())

    def exit_object(self) -> None:
        """Called when exiting an object context."""
        if self.object_stack:
            self.object_stack.pop()
