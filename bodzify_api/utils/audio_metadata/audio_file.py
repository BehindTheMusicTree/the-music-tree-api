
import os
import tempfile
from typing import Union

from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.db.models.fields.files import FieldFile


class AudioFile:
    def __init__(self, file: Union[TemporaryUploadedFile, FieldFile, InMemoryUploadedFile, str]):
        self.file = file
        print('file', file)
        print('file class', file.__class__)

        if isinstance(file, TemporaryUploadedFile):
            self.file_path = file.name
        elif isinstance(file, FieldFile):
            self.file_path = file.path
        elif isinstance(file, InMemoryUploadedFile):
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(file.read())
            temp_file.close()
            self.file_path = temp_file.name
        else:
            self.file_path = file

        if not os.path.exists(self.file_path):
            print('file does not exist')
            raise FileNotFoundError(f"File {self.file_path} does not exist")

        file_extension = os.path.splitext(
            self.file.name if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile))
            else self.file if isinstance(self.file, str)
            else str(self.file)
        )[1].lower()
        self.file_extension = file_extension
        print(file_extension)
        return

    def read(self, size: int = -1) -> bytes:
        with open(self.file_path, 'rb') as f:
            return f.read(size)

    def write(self, data: bytes) -> int:
        with open(self.file_path, 'wb') as f:
            return f.write(data)

    def seek(self, offset: int, whence: int = 0) -> int:
        with open(self.file_path, 'rb') as f:
            return f.seek(offset, whence)

    def close(self) -> None:
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile)):
            self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
