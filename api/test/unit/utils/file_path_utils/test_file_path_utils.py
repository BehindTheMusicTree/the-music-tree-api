import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest
from django.core.files import File as DjangoFile
from django.core.files.base import File as DjangoBaseFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models.fields.files import FieldFile

from api import settings
from api.utils.file_path_utils import (
    get_file_name_original,
    get_file_name_system,
    get_file_path,
)


class TestGetFilePath:
    def setup_method(self):
        """Create temp directory if it doesn't exist."""
        temp_dir = getattr(settings, 'FILE_UPLOAD_TEMP_DIR', '/tmp/pool')
        os.makedirs(temp_dir, exist_ok=True)

    def test_string_path_then_returns_string(self):
        file_path = "/path/to/file.mp3"
        assert get_file_path(file_path) == file_path

    def test_temporary_uploaded_file_then_returns_temporary_path(self):
        uploaded_file = TemporaryUploadedFile(
            name="test.mp3",
            content_type="audio/mpeg",
            size=12,
            charset=None,
        )
        tmp_path = uploaded_file.temporary_file_path()
        with open(tmp_path, 'wb') as f:
            f.write(b"test content")

        result = get_file_path(uploaded_file)
        assert os.path.exists(result)
        assert result == uploaded_file.temporary_file_path()

        uploaded_file.close()
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    def test_field_file_with_file_then_returns_file_name(self):
        field_file = Mock(spec=FieldFile)
        field_file.file = Mock()
        field_file.file.name = "/path/to/file.mp3"
        field_file.name = "file.mp3"

        assert get_file_path(field_file) == "/path/to/file.mp3"

    def test_field_file_without_file_then_returns_name(self):
        field_file = Mock(spec=FieldFile)
        field_file.file = None
        field_file.name = "/path/to/file.mp3"

        assert get_file_path(field_file) == "/path/to/file.mp3"

    def test_field_file_without_name_then_raises_value_error(self):
        field_file = Mock(spec=FieldFile)
        field_file.file = None
        field_file.name = None

        with pytest.raises(ValueError, match="FieldFile has no name"):
            get_file_path(field_file)

    def test_django_file_then_returns_name(self):
        django_file = Mock(spec=DjangoFile)
        django_file.name = "/path/to/file.mp3"
        django_file.file = None

        assert get_file_path(django_file) == "/path/to/file.mp3"

    def test_django_base_file_with_file_then_returns_file_name(self):
        django_file = Mock(spec=DjangoBaseFile)
        django_file.file = Mock()
        django_file.file.name = "/path/to/file.mp3"
        django_file.name = "file.mp3"

        assert get_file_path(django_file) == "/path/to/file.mp3"


class TestGetFileNameSystem:
    def setup_method(self):
        """Create temp directory if it doesn't exist."""
        temp_dir = getattr(settings, 'FILE_UPLOAD_TEMP_DIR', '/tmp/pool')
        os.makedirs(temp_dir, exist_ok=True)

    def test_string_path_then_returns_basename(self):
        file_path = "/path/to/file.mp3"
        assert get_file_name_system(file_path) == "file.mp3"

    def test_temporary_uploaded_file_then_returns_basename(self):
        uploaded_file = TemporaryUploadedFile(
            name="original.mp3",
            content_type="audio/mpeg",
            size=12,
            charset=None,
        )
        tmp_path = uploaded_file.temporary_file_path()
        with open(tmp_path, 'wb') as f:
            f.write(b"test content")

        result = get_file_name_system(uploaded_file)
        assert result == os.path.basename(uploaded_file.temporary_file_path())

        uploaded_file.close()
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


class TestGetFileNameOriginal:
    def test_string_path_then_returns_string(self):
        file_path = "/path/to/file.mp3"
        assert get_file_name_original(file_path) == file_path

    def test_temporary_uploaded_file_then_returns_name(self):
        uploaded_file = TemporaryUploadedFile(
            name="original.mp3",
            content_type="audio/mpeg",
            size=12,
            charset=None,
        )
        assert get_file_name_original(uploaded_file) == "original.mp3"

    def test_field_file_then_returns_name(self):
        field_file = Mock(spec=FieldFile)
        field_file.name = "file.mp3"
        assert get_file_name_original(field_file) == "file.mp3"

    def test_django_file_then_returns_name(self):
        django_file = Mock(spec=DjangoFile)
        django_file.name = "file.mp3"
        assert get_file_name_original(django_file) == "file.mp3"

    def test_unsupported_type_then_raises_not_implemented_error(self):
        unsupported = object()
        with pytest.raises(NotImplementedError):
            get_file_name_original(unsupported)
