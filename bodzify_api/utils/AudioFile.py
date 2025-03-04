
import json
import os
import subprocess
import tempfile
from typing import Union, cast

from django.core.exceptions import ImproperlyConfigured
from django.core.files import File as DjangoFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.files.base import File as DjangoBaseFile
from django.db.models.fields.files import FieldFile
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

from bodzify_api import settings
from bodzify_api.utils.audio_metadata.exceptions import FileByteMismatchError, FileCorruptedError


class AudioFile:

    file: TemporaryUploadedFile | FieldFile | InMemoryUploadedFile | str
    file_path: str | None

    def __init__(self, file: Union[TemporaryUploadedFile, FieldFile, InMemoryUploadedFile, str]):

        if isinstance(file, FieldFile):
            file = file.file or file.name

        self.file = file

        if isinstance(file, TemporaryUploadedFile):
            self.file_path = file.temporary_file_path()
        elif isinstance(file, InMemoryUploadedFile):
            self.file_path = None
        elif isinstance(file, DjangoBaseFile):
            self.file_path = file.file.name
        elif isinstance(file, DjangoFile):
            self.file_path = file.name
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
        return

    def get_duration_in_sec(self) -> float:
        path = self.get_file_path_or_object()

        if self.file_extension == '.mp3':
            try:
                audio = MP3(path)
                duration = audio.info.length
            except Exception as exc:
                # If MP3 fails, try other formats as fallback
                try:
                    return WAVE(path).info.length
                except:
                    try:
                        return FLAC(path).info.length
                    except:
                        raise exc  # If all attempts fail, raise original MP3 error

        elif self.file_extension == '.wav':
            try:
                # Use ffprobe to get duration, more tolerant of file format issues
                result = subprocess.run([
                    'ffprobe',
                    '-v', 'quiet',
                    '-print_format', 'json',
                    '-show_format',
                    '-show_streams',
                    path
                ], capture_output=True, text=True)

                if result.returncode != 0:
                    raise RuntimeError("Failed to probe audio file")

                data = json.loads(result.stdout)
                # Try format duration first, then stream duration if available
                duration = float(data.get('format', {}).get('duration') or
                                 next((s.get('duration') for s in data.get('streams', [])
                                       if s.get('duration')), 0))

                if duration <= 0:
                    raise RuntimeError("Could not determine audio duration")

            except json.JSONDecodeError:
                raise RuntimeError("Failed to parse audio file metadata")
            except Exception as exc:
                if str(exc) == "Failed to probe audio file":
                    raise FileCorruptedError("ffprobe could not parse the audio file.")
                raise RuntimeError(f"Failed to read WAV file duration: {str(exc)}")

        elif self.file_extension == '.flac':
            try:
                duration = FLAC(path).info.length
            except Exception as exc:
                error_str = str(exc)
                if "file said" in error_str and "bytes, read" in error_str:
                    raise FileByteMismatchError(error_str.capitalize())
                raise
        else:
            raise NotImplementedError(f"Reading is not supported for file type: {type(self.file)}")

        return duration if duration > 1 else 1

    def get_bitrate(self) -> int:
        path = self.get_file_path_or_object()
        if self.file_extension == '.mp3':
            audio = MP3(path)
            # Calculate MP3 bitrate from file size and duration
            if audio.info.length > 0 and isinstance(path, str) and os.path.exists(path):
                file_size = os.path.getsize(path)
                return int((file_size * 8) / self.get_duration_in_sec() / 1000)
            return 0
        elif self.file_extension == '.wav':
            try:
                # Use ffprobe to get audio stream information
                result = subprocess.run([
                    'ffprobe',
                    '-v', 'quiet',
                    '-print_format', 'json',
                    '-show_streams',
                    '-select_streams', 'a:0',  # Select first audio stream
                    path
                ], capture_output=True, text=True)

                if result.returncode != 0:
                    raise RuntimeError("Failed to probe audio file")

                data = json.loads(result.stdout)
                if not data.get('streams'):
                    raise RuntimeError("No audio streams found")

                stream = data['streams'][0]
                # Get bitrate directly if available
                if 'bit_rate' in stream:
                    return int(stream['bit_rate']) // 1000

                # Calculate from sample_rate * channels * bits_per_sample if no direct bitrate
                sample_rate = int(stream.get('sample_rate', 0))
                channels = int(stream.get('channels', 0))
                bits_per_sample = int(stream.get('bits_per_raw_sample', 0) or stream.get('bits_per_sample', 0))

                if not all([sample_rate, channels, bits_per_sample]):
                    raise RuntimeError("Missing audio stream information")

                return (sample_rate * channels * bits_per_sample) // 1000
            except json.JSONDecodeError:
                raise RuntimeError("Failed to parse audio file metadata")
            except Exception as exc:
                raise RuntimeError(f"Failed to read WAV file bitrate: {str(exc)}")
        elif self.file_extension == '.flac':
            audio = FLAC(path)
            # FLAC bitrate = sample_rate * channels * bits_per_sample
            return (audio.info.sample_rate * audio.info.channels *
                    audio.info.bits_per_sample) // 1000
        else:
            raise NotImplementedError(f"Reading is not supported for file type: {type(self.file)}")

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
        if isinstance(self.file, InMemoryUploadedFile):
            # For InMemoryUploadedFile, we can directly use the file object
            return self.file.seek(offset, whence)
        elif self.file_path is not None:
            with open(self.file_path, 'rb') as f:
                return f.seek(offset, whence)
        else:
            raise NotImplementedError(f"Seeking is not supported for file type: {type(self.file)}")

    def close(self) -> None:
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile)):
            self.file.close()
        else:
            raise NotImplementedError(f"Closing is not supported for file type: {type(self.file)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_file_path_or_object(self) -> str:
        """
        Returns a path to the file on the filesystem.
        For InMemoryUploadedFile, creates a temporary file in Django's upload directory.
        """
        if isinstance(self.file, (InMemoryUploadedFile)):
            from django.conf import settings
            temp_dir = settings.FILE_UPLOAD_TEMP_DIR
            if temp_dir:
                temp_file = tempfile.NamedTemporaryFile(dir=temp_dir, delete=False)
            else:
                # Fallback to system default if Django temp dir not configured
                temp_file = tempfile.NamedTemporaryFile(delete=False)
            for chunk in self.file.chunks():
                temp_file.write(chunk)
            temp_file.close()
            return temp_file.name
        else:
            return self.file_path  # type: ignore  # We validate in __init__ that it exists and is str

    def get_file_name_original(self):
        """
        "Original" means the name of the file that was uploaded by the user.
        The actual file name may be different if the file was renamed during the upload process.
        """
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile, DjangoFile)):
            return self.file.name
        elif isinstance(self.file, str):
            return self.file
        else:
            raise NotImplementedError(f"Reading is not supported for file type: {type(self.file)}")

    def get_file_name_system(self):
        """
        Returns the actual filename in the system, which may be different from the original name
        if the file was renamed during upload or processing.
        For InMemoryUploadedFile, creates a temporary file and returns its path.
        """
        path = self.get_file_path_or_object()  # This handles creating temp file for InMemoryUploadedFile
        return os.path.basename(path)

    def is_flac_file_md5_valid(self) -> bool:
        if not self.file_extension == '.flac':
            raise ImproperlyConfigured("The file is not a FLAC file")

        if isinstance(self.file, InMemoryUploadedFile):
            # Create a temporary file for validation
            temp_dir = settings.FILE_UPLOAD_TEMP_DIR
            with tempfile.NamedTemporaryFile(dir=temp_dir if temp_dir else None, delete=False) as temp_file:
                temp_path = temp_file.name
                self.file.seek(0)
                temp_file.write(self.read())

            try:
                # Validate the temporary file
                result = subprocess.run(['flac', '-t', temp_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                os.unlink(temp_path)  # Clean up
            except Exception as e:
                os.unlink(temp_path)  # Clean up even on error
                raise e

            # Reset file position for future operations
            self.file.seek(0)
        else:
            # Then the file path is not None
            file_path: str = self.file_path  # type: ignore
            result = subprocess.run(['flac', '-t', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = result.stderr.decode()
        if 'ok' in output:
            return True
        if 'MD5 signature mismatch' in output:
            return False
        if 'FLAC__STREAM_DECODER_ERROR_STATUS_LOST_SYNC' in output:
            return False
        else:
            raise FileCorruptedError("The Flac file md5 check failed")

    def get_file_with_corrected_md5(self) -> InMemoryUploadedFile | str:
        """
        Returns a new file with corrected MD5 signature.
        For InMemoryUploadedFile, returns a new InMemoryUploadedFile instance.
        For file-based files, returns the path to the corrected file.
        """
        # Create a temporary file to store the corrected FLAC content
        temp_dir = settings.FILE_UPLOAD_TEMP_DIR
        with tempfile.NamedTemporaryFile(dir=temp_dir if temp_dir else None, delete=False) as temp_file:
            temp_path = temp_file.name

        if isinstance(self.file, InMemoryUploadedFile):
            self.file.seek(0)
            result = subprocess.run(['flac', '-f', '--best', '-o', temp_path, '-'],
                                    input=self.read(),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        else:
            # The file path is not None
            file_path = cast(str, self.file_path)
            with open(file_path, 'rb') as f:
                result = subprocess.run(['flac', '-f', '--best', '-o', temp_path, '-'],
                                        input=f.read(),
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

        stderr = result.stderr.decode()
        if 'wrote' not in stderr:
            os.unlink(temp_path)  # Clean up on error
            raise FileCorruptedError(
                "The Flac file md5 check failed and could not be corrected. The file is probably corrupted.")

        if isinstance(self.file, InMemoryUploadedFile):
            # Read the corrected content
            with open(temp_path, 'rb') as f:
                corrected_content = f.read()

            # Create a new InMemoryUploadedFile with the corrected content
            from io import BytesIO
            file_obj = BytesIO()
            file_obj.write(corrected_content)
            file_obj.seek(0)  # Reset position for reading

            original_file = cast(InMemoryUploadedFile, self.file)

            # Create new file with same metadata as original
            new_file = InMemoryUploadedFile(
                file=file_obj,
                field_name=original_file.field_name or None,
                name=original_file.name,
                content_type=original_file.content_type or 'audio/x-flac',
                size=len(corrected_content),
                charset=original_file.charset,
                content_type_extra=original_file.content_type_extra or {}
            )

            # Clean up and verify
            os.unlink(temp_path)

            # Create temporary AudioFile to verify the fix worked
            temp_audio_file = AudioFile(new_file)
            if not temp_audio_file.is_flac_file_md5_valid():
                raise FileCorruptedError("Failed to fix FLAC MD5 signature")

            return new_file
        else:
            # For file-based files, return the path to the corrected file
            return temp_path
