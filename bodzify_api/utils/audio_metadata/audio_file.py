
import os
from typing import Union

from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.db.models.fields.files import FieldFile


class AudioFile:
    def __init__(self, file: Union[TemporaryUploadedFile, FieldFile, InMemoryUploadedFile, str]):
        self.file = file
        file_extension = os.path.splitext(
            self.file.name if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile))
            else self.file if isinstance(self.file, str)
            else str(self.file)
        )[1].lower()
        self.file_extension = file_extension

    def read(self, size: int = -1) -> bytes:
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile)):
            return self.file.read(size)
        else:
            # Assume file is a file path
            with open(self.file, 'rb') as f:
                return f.read(size)

    def write(self, data: bytes) -> int:
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile)):
            return self.file.write(data)
        else:
            # Assume file is a file path
            with open(self.file, 'wb') as f:
                return f.write(data)

    def seek(self, offset: int, whence: int = 0) -> int:
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile)):
            return self.file.seek(offset, whence)
        else:
            # Assume file is a file path
            with open(self.file, 'rb') as f:
                return f.seek(offset, whence)

    def close(self) -> None:
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile)):
            self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
