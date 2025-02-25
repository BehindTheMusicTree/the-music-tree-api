
from django.core.files import File


class AppDjangoFile(File):
    """Custom Django File class with additional functionality."""

    def __init__(self, file_abs_path: str, *args, **kwargs):
        """Initialize the file with its absolute path."""
        self.file_abs_path = file_abs_path
        with open(file_abs_path, 'rb') as f:
            super().__init__(f, *args, **kwargs)
