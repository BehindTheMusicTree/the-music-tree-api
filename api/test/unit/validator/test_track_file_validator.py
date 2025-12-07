from unittest.mock import MagicMock, Mock, patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.exception.validation.app.AppValidationException import AppValidationException
from api.validator.TrackFileValidator import TrackFileValidator


class TestTrackFileValidator:
    def test_valid_mp3_extension_then_passes(self):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.mp3", b"fake content", content_type="audio/mpeg")

        with patch.object(validator, "_validate_file_size"), patch.object(
            validator, "_validate_content_type_is_audio_from_magic_bytes_and_content"
        ):
            validator(file)

    def test_invalid_extension_then_raises_app_validation_exception(self):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.txt", b"fake content", content_type="text/plain")

        with pytest.raises(AppValidationException) as exc_info:
            validator(file)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID

    def test_file_too_large_then_raises_app_validation_exception(self):
        from api import settings
        validator = TrackFileValidator()
        max_size_bytes = settings.UPLOADED_TRACK_FILE_SIZE_MAX_IN_MO * 1000000
        large_content = b"x" * (max_size_bytes + 1)
        file = SimpleUploadedFile("test.mp3", large_content, content_type="audio/mpeg")

        with patch.object(validator, "_validate_extension"), patch.object(
            validator, "_validate_content_type_is_audio_from_magic_bytes_and_content"
        ):
            with pytest.raises(AppValidationException) as exc_info:
                validator(file)

            assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.FILE_TOO_LARGE

    def test_file_too_small_then_raises_app_validation_exception(self):
        from api import settings
        validator = TrackFileValidator()
        min_size_bytes = settings.UPLOADED_TRACK_FILE_SIZE_MIN_IN_MO * 1000000
        if min_size_bytes > 0:
            tiny_content = b"x" * (min_size_bytes - 1)
            file = SimpleUploadedFile("test.mp3", tiny_content, content_type="audio/mpeg")

            with patch.object(validator, "_validate_extension"), patch.object(
                validator, "_validate_content_type_is_audio_from_magic_bytes_and_content"
            ):
                with pytest.raises(AppValidationException) as exc_info:
                    validator(file)

                assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.FILE_TOO_SMALL
        else:
            pytest.skip("Minimum file size is 0, cannot test 'too small' scenario")

    def test_id3_magic_bytes_then_passes(self):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.mp3", b"ID3\x04\x00", content_type="audio/mpeg")
        file.size = 1024 * 1024

        with patch.object(validator, "_validate_extension"), patch.object(validator, "_validate_file_size"):
            validator(file)

    def test_riff_magic_bytes_then_passes(self):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.wav", b"RIFF", content_type="audio/wav")
        file.size = 1024 * 1024

        with patch.object(validator, "_validate_extension"), patch.object(validator, "_validate_file_size"):
            validator(file)

    @patch("api.validator.TrackFileValidator.audiometa.get_unified_metadata")
    @patch("api.validator.TrackFileValidator.get_file_path")
    def test_valid_audio_file_then_passes(self, mock_get_path, mock_get_metadata):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.mp3", b"fake content", content_type="audio/mpeg")
        file.size = 1024 * 1024
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_get_metadata.return_value = {}

        with patch.object(validator, "_validate_extension"), patch.object(validator, "_validate_file_size"):
            validator(file)

        mock_get_metadata.assert_called_once()

    @patch("api.validator.TrackFileValidator.audiometa.get_unified_metadata")
    @patch("api.validator.TrackFileValidator.get_file_path")
    def test_invalid_audio_file_then_raises_app_validation_exception(
        self, mock_get_path, mock_get_metadata
    ):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.mp3", b"fake content", content_type="audio/mpeg")
        file.size = 1024 * 1024
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_get_metadata.side_effect = Exception("Not an audio file")

        with patch.object(validator, "_validate_extension"), patch.object(validator, "_validate_file_size"):
            with pytest.raises(AppValidationException) as exc_info:
                validator(file)

            assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.TRACK_FILE_TYPE_INVALID
