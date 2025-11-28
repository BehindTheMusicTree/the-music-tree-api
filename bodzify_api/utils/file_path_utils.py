import os
from typing import TypeAlias

from django.core.files import File as DjangoFile
from django.core.files.base import File as DjangoBaseFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models.fields.files import FieldFile

DiskBasedFile: TypeAlias = TemporaryUploadedFile | FieldFile | str


def get_file_path(file: DiskBasedFile | DjangoFile) -> str:
    """Convert file to path string."""
    if isinstance(file, FieldFile):
        if file.file:
            return file.file.name
        name = file.name
        if name is None:
            raise ValueError("FieldFile has no name")
        return name
    if isinstance(file, TemporaryUploadedFile):
        return file.temporary_file_path()
    if isinstance(file, (DjangoBaseFile, DjangoFile)):
        return file.file.name if hasattr(file, 'file') and file.file else file.name
    return str(file)


def get_file_name_system(file: DiskBasedFile | DjangoFile) -> str:
    """Returns the actual filename in the system."""
    file_path = get_file_path(file)
    return os.path.basename(file_path)


def get_file_name_original(file: DiskBasedFile | DjangoFile) -> str:
    """
    Returns the original filename that was uploaded by the user.
    The actual file name may be different if the file was renamed during the upload process.
    """
    if isinstance(file, (TemporaryUploadedFile, FieldFile, DjangoFile)):
        return file.name
    elif isinstance(file, str):
        return file
    else:
        raise NotImplementedError(f"Reading is not supported for file type: {type(file)}")

