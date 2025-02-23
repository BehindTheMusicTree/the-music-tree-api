
import os
import tempfile
from typing import Union

from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.db.models.fields.files import FieldFile
from django.core.files import File as DjangoFile


class AudioFile:
    def __init__(self, file: Union[TemporaryUploadedFile, FieldFile, InMemoryUploadedFile, str]):
        self.file = file
        print('file', file)
        print('file class', file.__class__)

        if isinstance(file, FieldFile):
            file = file.file

        if isinstance(file, TemporaryUploadedFile):
            self.file_path = file.file.name
        elif isinstance(file, TemporaryUploadedFile):
            self.file_path = file.temporary_file_path()
        elif isinstance(file, DjangoFile):
            self.file_path = file.name
        elif isinstance(file, InMemoryUploadedFile):
            self.file_path = None
        else:
            self.file_path = file

        if self.file_path is not None and not os.path.exists(self.file_path):
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
        if isinstance(self.file, InMemoryUploadedFile):
            return self.file.read(size)
        elif self.file_path is not None:
            with open(self.file_path, 'rb') as f:
                return f.read(size)
        else:
            raise NotImplementedError(f"Reading is not supported for file type: {type(self.file)}")

    def write(self, data: bytes) -> int:
        if isinstance(self.file, InMemoryUploadedFile):
            return self.file.write(data)
        elif self.file_path is not None:
            with open(self.file_path, 'wb') as f:
                return f.write(data)
        else:
            raise NotImplementedError(f"Writing is not supported for file type: {type(self.file)}")

    def seek(self, offset: int, whence: int = 0) -> int:
        if self.file_path is not None:
            with open(self.file_path, 'rb') as f:
                return f.seek(offset, whence)
        else:
            raise NotImplementedError(f"Seeking is not supported for file type: {type(self.file)}")

    def close(self) -> None:
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile)):
            self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_file_path_or_object(self):
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile)):
            return self.file_path
        elif isinstance(self.file, InMemoryUploadedFile):
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            for chunk in self.file.chunks():
                temp_file.write(chunk)
            temp_file.close()
            return temp_file.name
        else:
            return self.file_path

    def get_file_name(self):
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile)):
            return self.file.name
        else:
            return self.file
