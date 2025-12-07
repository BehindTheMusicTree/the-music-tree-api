import os
from typing import TypeAlias

from django.core.files import File as DjangoFile
from django.core.files.base import File as DjangoBaseFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models.fields.files import FieldFile

from api import settings

DiskBasedFile: TypeAlias = TemporaryUploadedFile | FieldFile | str


def get_file_path(file: DiskBasedFile | DjangoFile) -> str:
    """Convert file to path string."""
    if isinstance(file, FieldFile):
        if file.file:
            if isinstance(file.file, TemporaryUploadedFile):
                return file.file.temporary_file_path()
            if hasattr(file.file, 'name'):
                file_name = file.file.name
                if os.path.isabs(file_name):
                    if os.path.exists(file_name):
                        return file_name
            if hasattr(file, 'path'):
                file_path = file.path
                if not os.path.isabs(file_path):
                    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                    if os.path.exists(full_path):
                        return full_path
                    return os.path.join(settings.MEDIA_ROOT, file_path)
                if os.path.exists(file_path):
                    return file_path
            if hasattr(file.file, 'name'):
                file_name = file.file.name
                if os.path.isabs(file_name):
                    return file_name
                return file_name
        name = file.name
        if name is None:
            raise ValueError("FieldFile has no name")
        if hasattr(file, 'path'):
            file_path = file.path
            if not os.path.isabs(file_path):
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                if os.path.exists(full_path):
                    return full_path
                return os.path.join(settings.MEDIA_ROOT, file_path)
            if os.path.exists(file_path):
                return file_path
        return name
    if isinstance(file, TemporaryUploadedFile):
        return file.temporary_file_path()
    if isinstance(file, (DjangoBaseFile, DjangoFile)):
        if hasattr(file, 'file') and file.file:
            if hasattr(file.file, 'name'):
                file_name = file.file.name
                if os.path.isabs(file_name) and os.path.exists(file_name):
                    return file_name
        if hasattr(file, 'name'):
            name = file.name
            if os.path.isabs(name) and os.path.exists(name):
                return name
            return name
        return str(file)
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
